from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Student
from .models import Admin
from .models import Enseignant
from .models import Filiere
from .models import Cours
from .models import Paiement
from .models import EmploiDuTemps
from .models import Presence
import datetime
from django.http import JsonResponse
from .models import Evaluation
from .models import Note

import hashlib


def accueil(request):
    return render(request, 'accueil.html')


def connexion_etudiant(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            etudiant = Student.objects.get(email=email, password=password_hash)
            request.session['etudiant_id'] = etudiant.id
            request.session['etudiant_nom'] = etudiant.nom + ' ' + etudiant.prenom
            request.session['etudiant_role'] = etudiant.role
            return redirect('dashboard_admin')
        except Student.DoesNotExist:
            messages.error(request, 'Email ou mot de passe incorrect !')
    return render(request, 'connexion_etudiant.html')


def dashboard_admin(request):
    if not request.session.get('admin_id') \
            and not request.session.get('etudiant_id') \
            and not request.session.get('enseignant_id'):
        return redirect('login_admin')

    nom = (
            request.session.get('etudiant_nom') or
            request.session.get('enseignant_nom') or
            "ADMIN"
    )

    role = (
            request.session.get('etudiant_role') or
            request.session.get('enseignant_role') or
            request.session.get('admin_role')
    )

    # 🔥 STATISTIQUES RÉELLES
    total_etudiants = Student.objects.count()
    total_enseignants = Enseignant.objects.count()
    total_paiements = Paiement.objects.count()

    # 💡 impayés = reste à payer > 0
    impayes = Paiement.objects.filter(reste_a_payer__gt=0).count()

    return render(request, 'dashboard_admin.html', {
        'active_page': 'dashboard_admin',
        'nom': nom,
        'role': role,

        #  DATA POUR LE HTML
        'total_etudiants': total_etudiants,
        'total_enseignants': total_enseignants,
        'total_paiements': total_paiements,
        'impayes': impayes
    })


def students(request):
    liste_filieres = Filiere.objects.all()

    if request.method == 'POST':
        etudiant_id = request.POST.get('id')  # 🔥 pour UPDATE
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        date_naissance = request.POST.get('date_naissance')
        sexe = request.POST.get('sexe')
        adresse = request.POST.get('adresse')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        filiere_id = request.POST.get('filiere')
        nom_parent = request.POST.get('nom_parent')
        telephone_parent = request.POST.get('telephone_parent')
        photo = request.FILES.get('photo')
        formation = request.POST.get('formation')

        # 🔴 sécuriser filière
        if not filiere_id:
            messages.error(request, "Veuillez choisir une filière")
            return redirect('etudiants')

        try:
            filiere = Filiere.objects.get(id=filiere_id)
        except Filiere.DoesNotExist:
            messages.error(request, "Filière invalide")
            return redirect('etudiants')

        # 🔥 MODE UPDATE
        if etudiant_id:
            try:
                etudiant = Student.objects.get(id=etudiant_id)

                etudiant.nom = nom
                etudiant.prenom = prenom
                etudiant.date_naissance = date_naissance
                etudiant.sexe = sexe
                etudiant.adresse = adresse
                etudiant.telephone = telephone
                etudiant.email = email
                etudiant.filiere = filiere
                etudiant.nom_parent = nom_parent
                etudiant.telephone_parent = telephone_parent
                etudiant.formation = formation

                if password:
                    etudiant.password = hashlib.sha256(password.encode()).hexdigest()

                if photo:
                    etudiant.photo = photo

                etudiant.save()

                messages.success(request, "Etudiant modifié avec succès")
                return redirect('etudiants')

            except Student.DoesNotExist:
                messages.error(request, "Etudiant introuvable")
                return redirect('etudiants')

        # 🔥 MODE CREATE
        else:
            if Student.objects.filter(email=email).exists():
                messages.error(request, "Cet email existe déjà !")
                return redirect('etudiants')

            password_hash = hashlib.sha256(password.encode()).hexdigest()

            Student.objects.create(
                nom=nom,
                prenom=prenom,
                date_naissance=date_naissance,
                sexe=sexe,
                adresse=adresse,
                telephone=telephone,
                email=email,
                password=password_hash,
                filiere=filiere,
                nom_parent=nom_parent,
                telephone_parent=telephone_parent,
                photo=photo,
                formation=formation
            )

            messages.success(request, "Etudiant inscrit avec succès")
            return redirect('etudiants')

    liste_etudiants = Student.objects.all().order_by('nom')
    return render(request, 'etudiants.html', {
        'etudiants': liste_etudiants,
        'filieres': liste_filieres
    })


def dashboard_admin(request):
    if not request.session.get('admin_id') \
            and not request.session.get('etudiant_id') \
            and not request.session.get('enseignant_id'):
        return redirect('login_admin')

    nom = (
            request.session.get('etudiant_nom') or
            request.session.get('enseignant_nom') or
            "ADMIN"
    )
    role = (
            request.session.get('etudiant_role') or
            request.session.get('enseignant_role') or
            request.session.get('admin_role')
    )

    total_etudiants = Student.objects.count()
    total_enseignants = Enseignant.objects.count()
    total_paiements = Paiement.objects.count()
    impayes = Paiement.objects.filter(reste_a_payer__gt=0).count()

    # Pour les modals actions rapides
    filieres = Filiere.objects.all()
    enseignants = Enseignant.objects.all()
    etudiants = Student.objects.all()

    return render(request, 'dashboard_admin.html', {
        'active_page': 'dashboard_admin',
        'nom': nom,
        'role': role,
        'total_etudiants': total_etudiants,
        'total_enseignants': total_enseignants,
        'total_paiements': total_paiements,
        'impayes': impayes,
        'filieres': filieres,
        'enseignants': enseignants,
        'etudiants': etudiants,
    })


def login_admin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        try:
            admin = Admin.objects.get(email=email, password=password_hash)
            request.session['admin_id'] = admin.id
            return redirect('dashboard_admin')
        except Admin.DoesNotExist:
            messages.error(request, "Email ou mot de passe incorrect")

    return render(request, 'login_admin.html')


def deconnexion_etudiant(request):
    request.session.flush()
    return redirect('connexion_etudiant')


def inscription_admin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if Admin.objects.filter(email=email).exists():
            messages.error(request, "Email déjà utilisé")
            return redirect('inscription_admin')

        Admin.objects.create(email=email, password=password_hash)
        messages.success(request, "Compte créé avec succès")
        return redirect('login_admin')

    return render(request, 'inscription_admin.html')


def login_admin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        try:
            admin = Admin.objects.get(email=email, password=password_hash)
            request.session['admin_id'] = admin.id
            request.session['admin_role'] = admin.role

            return redirect('dashboard_admin')

        except Admin.DoesNotExist:
            messages.error(request, "Identifiants incorrects")

    return render(request, 'login_admin.html')


def enseignants(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        date_naissance = request.POST.get('date_naissance')
        sexe = request.POST.get('sexe')
        adresse = request.POST.get('adresse')
        photo = request.FILES.get('photo')

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if Enseignant.objects.filter(email=email).exists():
            messages.error(request, "Email déjà utilisé")
            return redirect('enseignants')

        Enseignant.objects.create(
            nom=nom,
            prenom=prenom,
            telephone=telephone,
            email=email,
            password=password_hash,
            date_naissance=date_naissance,
            sexe=sexe,
            adresse=adresse,
            photo=photo,

        )
        messages.success(request, "Enseignant ajouté avec succès")
        return redirect('enseignants')

    liste_enseignants = Enseignant.objects.all()
    return render(request, 'enseignants.html', {'enseignants': liste_enseignants})


def connexion_enseignant(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        try:
            enseignant = Enseignant.objects.get(email=email, password=password_hash)
            request.session['enseignant_id'] = enseignant.id
            request.session['enseignant_nom'] = enseignant.nom
            request.session['enseignant_role'] = enseignant.role

            return redirect('dashboard_admin')

        except Enseignant.DoesNotExist:
            messages.error(request, "Identifiants incorrects")

    return render(request, 'connexion_enseignant.html')


def filieres(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        duree = request.POST.get('duree')
        frais_total = request.POST.get('frais_total')

        if Filiere.objects.filter(nom=nom).exists():
            messages.error(request, "Cette filière existe déjà !")
        else:
            Filiere.objects.create(
                nom=nom,
                duree=duree,
                frais_total=frais_total
            )
            messages.success(request, "Filière ajoutée avec succès !")
        return redirect('filieres')

    # GET -> afficher toutes les filières
    liste_filieres = Filiere.objects.all()
    return render(request, 'filieres.html', {'filieres': liste_filieres})


def cours(request):
    erreur = None

    if request.method == "POST":
        nom = request.POST.get("nom")
        code = request.POST.get("code")
        enseignant_id = request.POST.get("enseignant")
        filiere_id = request.POST.get("filiere")

        if not nom or not enseignant_id or not filiere_id:
            erreur = "Tous les champs sont obligatoires."
        else:
            if Cours.objects.filter(code=code).exists():
                erreur = "Ce code de cours existe déjà."
            else:
                enseignant = Enseignant.objects.get(id=enseignant_id)
                filiere = Filiere.objects.get(id=filiere_id)

                Cours.objects.create(
                    nom=nom,
                    code=code,
                    enseignant=enseignant,
                    filiere=filiere
                )
                return redirect('cours')

    liste_cours = Cours.objects.select_related('enseignant', 'filiere').all().order_by('-id')
    liste_enseignants = Enseignant.objects.all()
    liste_filieres = Filiere.objects.all()

    return render(request, 'cours.html', {
        'cours_list': liste_cours,
        'enseignants': liste_enseignants,
        'filieres': liste_filieres,
        'erreur': erreur
    })


def paiements(request):
    if request.method == 'POST':
        etudiant_id = request.POST.get('etudiant_id')
        montant = request.POST.get('montant_verse')
        date_paie = request.POST.get('date_paiement')
        frais_total = request.POST.get('frais_total')
        deja_paye = request.POST.get('deja_paye')

        etudiant = Student.objects.get(id=etudiant_id)

        # Calcul reste à payer
        reste = float(frais_total) - float(deja_paye) - float(montant)

        # Numéro reçu automatique
        numero = f"RECU-{datetime.datetime.now().year}-{str(Paiement.objects.count() + 1).zfill(3)}"

        paiement = Paiement.objects.create(
            etudiant=etudiant,
            montant_verse=montant,
            date_paiement=date_paie,
            frais_total=frais_total,
            deja_paye=deja_paye,
            reste_a_payer=reste,
            numero_recu=numero,
        )

        messages.success(request, 'Paiement enregistré avec succès !')
        return redirect('recu_paiement', id=paiement.id)

    liste_paiements = Paiement.objects.all().order_by('-date_paiement')
    etudiants_liste = Student.objects.all()
    return render(request, 'paiements.html', {
        'paiements': liste_paiements,
        'etudiants': etudiants_liste,
    })


def recu_paiement(request, id):
    paiement = Paiement.objects.get(id=id)
    return render(request, 'recu_paiement.html', {'paiement': paiement})


def emploi_du_temps(request):
    erreur = None

    if request.method == "POST":
        cours_id = request.POST.get("cours")
        enseignant_id = request.POST.get("enseignant")
        filiere_id = request.POST.get("filiere")
        date = request.POST.get("date")
        heure_debut = request.POST.get("heure_debut")
        heure_fin = request.POST.get("heure_fin")

        if not cours_id or not enseignant_id or not filiere_id or not heure_debut or not heure_fin:
            erreur = "Tous les champs sont obligatoires."
        else:
            cours = Cours.objects.get(id=cours_id)
            enseignant = Enseignant.objects.get(id=enseignant_id)
            filiere = Filiere.objects.get(id=filiere_id)

            EmploiDuTemps.objects.create(
                cours=cours,
                enseignant=enseignant,
                filiere=filiere,
                date=date,
                heure_debut=heure_debut,
                heure_fin=heure_fin
            )

            return redirect('emploi_du_temps')

    cours_list = Cours.objects.all()
    enseignants = Enseignant.objects.all()
    filieres = Filiere.objects.all()
    emplois = EmploiDuTemps.objects.select_related('cours', 'enseignant', 'filiere').all()

    return render(request, 'emploi_du_temps.html', {
        "emplois": emplois,
        'cours_list': cours_list,
        'enseignants': enseignants,
        'filieres': filieres,
        'erreur': erreur

    })


def emploi_events(request):
    emplois = EmploiDuTemps.objects.select_related('cours', 'enseignant', 'filiere').all()
    events = []

    for emploi in emplois:
        events.append({
            'title': f"{emploi.cours.nom} - {emploi.filiere.nom}",
            'start': f"{emploi.date}T{emploi.heure_debut}",
            'end': f"{emploi.date}T{emploi.heure_fin}",
            'extendedProps': {
                'enseignant': f"{emploi.enseignant.nom} {emploi.enseignant.prenom or ''}",
                'filiere': emploi.filiere.nom
            }
        })

    return JsonResponse(events, safe=False)


def evaluation_teacher(request):
    filieres = Filiere.objects.all()
    cours = Cours.objects.all()

    tab = request.GET.get("tab")
    filiere_id = request.GET.get("filiere")
    evaluation_id = request.GET.get("evaluation")

    evaluations = Evaluation.objects.all()
    etudiants = []
    notes_map = {}
    bulletin_data = []

    # ================= FILTRAGE NOTES =================
    if tab == "notes" and filiere_id:
        etudiants_qs = Student.objects.filter(filiere_id=filiere_id)

        if evaluation_id:
            notes = Note.objects.filter(evaluation_id=evaluation_id)
            notes_map = {str(n.etudiant_id): n.note for n in notes}

        etudiants = []
        for etudiant in etudiants_qs:
            etudiant.note_actuelle = notes_map.get(str(etudiant.id), '')
            etudiants.append(etudiant)

    # ================= FILTRAGE BULLETIN =================
    if tab == "bulletin" and filiere_id and evaluation_id:
        notes = Note.objects.filter(
            evaluation_id=evaluation_id
        ).select_related('etudiant', 'evaluation', 'evaluation__cours')

        for n in notes:
            bulletin_data.append({
                "student": n.etudiant,
                "coef": n.evaluation.coefficient,
                "note": n.note,
                "total": round(n.note * n.evaluation.coefficient, 2),
                "matiere": n.evaluation.cours.nom,
                "eval_id": n.evaluation.id,
                "note_id": n.id,
            })

    # ================= AJOUT EVALUATION =================
    if request.method == "POST" and "add_evaluation" in request.POST:
        Evaluation.objects.create(
            nom=request.POST.get("nom"),
            filiere_id=request.POST.get("filiere"),
            cours_id=request.POST.get("cours"),
            coefficient=request.POST.get("coefficient"),
            sequence=request.POST.get("sequence")
        )
        return redirect('evaluation_teacher')

    # ================= SAVE NOTES =================
    if request.method == "POST" and "save_notes" in request.POST:
        eval_id = request.POST.get("evaluation_id")
        for key, value in request.POST.items():
            if key.startswith("note_") and value:
                student_id = key.split("_")[1]
                Note.objects.update_or_create(
                    etudiant_id=student_id,
                    evaluation_id=eval_id,
                    defaults={"note": value}
                )
        referer = request.META.get('HTTP_REFERER', '')
        return redirect(referer if referer else 'evaluation_teacher')

    # ================= MODIFIER NOTE =================
    if request.method == "POST" and "modifier_note" in request.POST:
        note_id = request.POST.get("note_id")
        nouvelle_note = request.POST.get("nouvelle_note")
        etudiant_id_post = request.POST.get("etudiant_id")
        eval_id_post = request.POST.get("eval_id")

        if note_id:
            Note.objects.filter(id=note_id).update(note=nouvelle_note)
        else:
            Note.objects.update_or_create(
                etudiant_id=etudiant_id_post,
                evaluation_id=eval_id_post,
                defaults={"note": nouvelle_note}
            )
        referer = request.META.get('HTTP_REFERER', '')
        return redirect(referer if referer else 'evaluation_teacher')

    return render(request, "evaluation_teacher.html", {
        "filieres": filieres,
        "cours": cours,
        "evaluations": evaluations,
        "etudiants": etudiants,
        "notes_map": notes_map,
        "bulletin_data": bulletin_data,
        "sequences": ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
    })


def get_evaluations(request):
    filiere_id = request.GET.get('filiere_id')
    evaluations = Evaluation.objects.filter(filiere_id=filiere_id)

    data = list(evaluations.values('id', 'nom'))
    return JsonResponse(data, safe=False)


def bulletin_etudiant(request, etudiant_id):
    etudiant = Student.objects.get(id=etudiant_id)
    evaluation_id = request.GET.get("evaluation")
    evaluation = Evaluation.objects.get(id=evaluation_id)

    # Toutes les évaluations de la même filière et séquence
    evaluations_seq = Evaluation.objects.filter(
        filiere=etudiant.filiere,
        sequence=evaluation.sequence
    )

    lignes = []
    total_points = 0
    total_coef = 0

    for eval_ in evaluations_seq:
        note_obj = Note.objects.filter(etudiant=etudiant, evaluation=eval_).first()
        note_val = note_obj.note if note_obj else None
        points = round(note_val * eval_.coefficient, 2) if note_val is not None else 0
        total_points += points
        total_coef += eval_.coefficient

        lignes.append({
            "matiere": eval_.cours.nom,
            "coef": eval_.coefficient,
            "note": note_val,
            "points": points,
        })

    moyenne = round(total_points / total_coef, 2) if total_coef > 0 else 0

    # Calcul du rang
    tous_etudiants = Student.objects.filter(filiere=etudiant.filiere)
    moyennes = []
    for e in tous_etudiants:
        tp = 0
        tc = 0
        for ev in evaluations_seq:
            n = Note.objects.filter(etudiant=e, evaluation=ev).first()
            if n:
                tp += n.note * ev.coefficient
                tc += ev.coefficient
        moy = round(tp / tc, 2) if tc > 0 else 0
        moyennes.append((e.id, moy))

    moyennes.sort(key=lambda x: x[1], reverse=True)
    rang = next((i + 1 for i, (eid, _) in enumerate(moyennes) if eid == etudiant.id), 0)
    total_etudiants = len(moyennes)

    return render(request, "bulletin_etudiant.html", {
        "etudiant": etudiant,
        "evaluation": evaluation,
        "lignes": lignes,
        "total_points": total_points,
        "total_coef": total_coef,
        "moyenne": moyenne,
        "rang": rang,
        "total_etudiants": total_etudiants,
        "filiere_id": etudiant.filiere.id,
        "evaluation_id": evaluation_id,
    })


def delete_etudiant(request, id):
    etudiant = Student.objects.get(id=id)
    etudiant.delete()
    messages.success(request, "Étudiant supprimé avec succès")
    return redirect('etudiants')


def edit_etudiant(request, id):
    etudiant = Student.objects.get(id=id)
    filieres = Filiere.objects.all()

    if request.method == "POST":
        etudiant.nom = request.POST.get('nom')
        etudiant.prenom = request.POST.get('prenom')
        etudiant.date_naissance = request.POST.get('date_naissance')
        etudiant.sexe = request.POST.get('sexe')
        etudiant.adresse = request.POST.get('adresse')
        etudiant.telephone = request.POST.get('telephone')
        etudiant.email = request.POST.get('email')
        etudiant.formation = request.POST.get('formation')

        filiere_id = request.POST.get('filiere')
        etudiant.filiere = Filiere.objects.get(id=filiere_id)

        # password (optionnel)
        password = request.POST.get('password')
        if password:
            etudiant.password = hashlib.sha256(password.encode()).hexdigest()

        if request.FILES.get('photo'):
            etudiant.photo = request.FILES.get('photo')

        etudiant.save()

        messages.success(request, "Étudiant modifié avec succès")
        return redirect('etudiants')

    return render(request, 'edit_etudiant.html', {
        'etudiant': etudiant,
        'filieres': filieres
    })


def delete_enseignant(request, id):
    enseignant = Enseignant.objects.get(id=id)
    enseignant.delete()
    messages.success(request, "Enseignant supprimé avec succès")
    return redirect('enseignants')


def edit_enseignant(request, id):
    enseignant = Enseignant.objects.get(id=id)

    if request.method == "POST":
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        date_naissance = request.POST.get('date_naissance')
        sexe = request.POST.get('sexe')
        adresse = request.POST.get('adresse')
        password = request.POST.get('password')
        photo = request.FILES.get('photo')

        # Vérifier email uniquement si changé
        if email != enseignant.email and Enseignant.objects.filter(email=email).exists():
            messages.error(request, "Email déjà utilisé")
            return redirect('enseignants')

        enseignant.nom = nom
        enseignant.prenom = prenom
        enseignant.telephone = telephone
        enseignant.email = email
        enseignant.date_naissance = date_naissance
        enseignant.sexe = sexe
        enseignant.adresse = adresse

        if password:
            enseignant.password = hashlib.sha256(password.encode()).hexdigest()
        if photo:
            enseignant.photo = photo

        enseignant.save()
        messages.success(request, "Enseignant modifié avec succès")
        return redirect('enseignants')

    return redirect('enseignants')


def delete_filiere(request, id):
    filiere = Filiere.objects.get(id=id)
    filiere.delete()
    messages.success(request, "Filière supprimée avec succès")
    return redirect('filieres')


def edit_filiere(request, id):
    filiere = Filiere.objects.get(id=id)
    if request.method == "POST":
        nom = request.POST.get('nom')
        duree = request.POST.get('duree')
        frais_total = request.POST.get('frais_total')

        # Vérifier si nom existe déjà sur une AUTRE filière
        if Filiere.objects.filter(nom=nom).exclude(id=id).exists():
            messages.error(request, "Ce nom de filière existe déjà")
            return redirect('filieres')

        filiere.nom = nom
        filiere.duree = duree
        filiere.frais_total = frais_total
        filiere.save()
        messages.success(request, "Filière modifiée avec succès")
        return redirect('filieres')

    return redirect('filieres')


def delete_cours(request, id):
    cours = Cours.objects.get(id=id)
    cours.delete()
    messages.success(request, "Cours supprimé avec succès")
    return redirect('cours')


def edit_cours(request, id):
    cours_obj = Cours.objects.get(id=id)
    if request.method == "POST":
        nom = request.POST.get('nom')
        enseignant_id = request.POST.get('enseignant')
        filiere_id = request.POST.get('filiere')

        cours_obj.nom = nom
        cours_obj.enseignant = Enseignant.objects.get(id=enseignant_id)
        cours_obj.filiere = Filiere.objects.get(id=filiere_id)
        cours_obj.save()

        messages.success(request, "Cours modifié avec succès")
        return redirect('cours')

    return redirect('cours')


def emploitemps_enseignant(request):
    enseignant_id = request.session.get('enseignant_id')

    emplois = EmploiDuTemps.objects.filter(enseignant_id=enseignant_id)

    return render(request, 'emploitemps_enseignant.html', {
        "emplois": emplois,
    })


from django.http import JsonResponse


def emploienseignant_events(request):
    # 🔥 récupérer l'enseignant connecté
    enseignant_id = request.session.get('enseignant_id')

    if not enseignant_id:
        return JsonResponse([], safe=False)

    # 🔥 filtrer uniquement ses emplois
    emplois = EmploiDuTemps.objects.select_related(
        'cours', 'enseignant', 'filiere'
    ).filter(enseignant_id=enseignant_id)

    events = []

    for emploi in emplois:
        events.append({
            'title': f"{emploi.cours.nom} - {emploi.filiere.nom}",
            'start': f"{emploi.date}T{emploi.heure_debut}",
            'end': f"{emploi.date}T{emploi.heure_fin}",
            'extendedProps': {
                'enseignant': f"{emploi.enseignant.nom} {emploi.enseignant.prenom or ''}",
                'filiere': emploi.filiere.nom
            }
        })

    return JsonResponse(events, safe=False)


def presence_enseignant(request):
    enseignant_id = request.session.get('enseignant_id')

    if not enseignant_id:
        return redirect('connexion_enseignant')

    enseignant = Enseignant.objects.get(id=enseignant_id)

    emplois = EmploiDuTemps.objects.select_related(
        'cours', 'filiere', 'enseignant'
    ).filter(enseignant_id=enseignant_id)

    return render(request, 'presence_enseignant.html', {
        "emplois": emplois,
        "enseignant": enseignant
    })


def get_etudiants_filiere(request, filiere_id):
    etudiants = Student.objects.filter(filiere_id=filiere_id)

    data = [
        {
            "id": e.id,
            "nom": e.nom,
            "prenom": e.prenom
        }
        for e in etudiants
    ]

    return JsonResponse(data, safe=False)


from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def save_presence(request):
    data = json.loads(request.body)

    emploi_id = data.get("emploi_id")
    presences = data.get("presences")

    emploi = EmploiDuTemps.objects.get(id=emploi_id)

    for p in presences:
        etudiant_id = p["etudiant_id"]

        Presence.objects.update_or_create(
            emploi=emploi,
            etudiant_id=etudiant_id,
            defaults={
                "statut": p["statut"]
            }
        )

    return JsonResponse({"status": "ok"})


def presence_data(request, emploi_id):
    presences = Presence.objects.filter(
        emploi_id=emploi_id
    ).select_related('etudiant')

    # dictionnaire pour écraser doublons
    data_dict = {}

    for p in presences:
        data_dict[p.etudiant_id] = {
            "nom": f"{p.etudiant.nom} {p.etudiant.prenom}",
            "statut": p.statut
        }

    return JsonResponse(list(data_dict.values()), safe=False)


def mes_cours(request):
    if 'etudiant_id' not in request.session:
        return redirect('connexion_etudiant')

    etudiant = Student.objects.get(id=request.session['etudiant_id'])
    cours_list = Cours.objects.filter(
        filiere=etudiant.filiere
    ).select_related('enseignant', 'filiere')

    return render(request, 'mes_cours.html', {
        'etudiant': etudiant,
        'cours_list': cours_list,
    })


def mon_emploi_du_temps(request):
    if 'etudiant_id' not in request.session:
        return redirect('connexion_etudiant')

    etudiant = Student.objects.get(id=request.session['etudiant_id'])

    return render(request, 'mon_emploi_du_temps.html', {
        'etudiant': etudiant,
    })


def emploi_events_etudiant(request):
    etudiant_id = request.session.get('etudiant_id')
    if not etudiant_id:
        return JsonResponse([], safe=False)

    etudiant = Student.objects.get(id=etudiant_id)
    emplois = EmploiDuTemps.objects.select_related(
        'cours', 'enseignant', 'filiere'
    ).filter(filiere=etudiant.filiere)

    events = []
    for emploi in emplois:
        events.append({
            'title': f"{emploi.cours.nom}",
            'start': f"{emploi.date}T{emploi.heure_debut}",
            'end': f"{emploi.date}T{emploi.heure_fin}",
            'extendedProps': {
                'enseignant': f"{emploi.enseignant.nom} {emploi.enseignant.prenom or ''}",
                'filiere': emploi.filiere.nom,
                'cours': emploi.cours.nom,
            }
        })

    return JsonResponse(events, safe=False)

def mes_notes(request):
    if 'etudiant_id' not in request.session:
        return redirect('connexion_etudiant')

    etudiant = Student.objects.get(id=request.session['etudiant_id'])
    sequence = request.GET.get('sequence')

    sequences_dispo = Evaluation.objects.filter(
        filiere=etudiant.filiere
    ).values_list('sequence', flat=True).distinct().order_by('sequence')

    notes_data = []
    total_points = 0
    total_coef = 0

    if sequence:
        evaluations = Evaluation.objects.filter(
            filiere=etudiant.filiere,
            sequence=sequence
        ).select_related('cours')

        for eval_ in evaluations:
            note_obj = Note.objects.filter(
                etudiant=etudiant,
                evaluation=eval_
            ).first()
            points = round(note_obj.note * eval_.coefficient, 2) if note_obj else 0
            total_points += points
            total_coef += eval_.coefficient

            notes_data.append({
                'matiere': eval_.cours.nom,
                'coef': eval_.coefficient,
                'note': note_obj.note if note_obj else None,
                'points': points,
            })

    moyenne = round(total_points / total_coef, 2) if total_coef > 0 else 0

    return render(request, 'mes_notes.html', {
        'etudiant': etudiant,
        'sequences': sequences_dispo,
        'sequence_selectionnee': sequence,
        'notes_data': notes_data,
        'total_points': total_points,
        'total_coef': total_coef,
        'moyenne': moyenne,
    })

def mes_bulletins(request):
    if 'etudiant_id' not in request.session:
        return redirect('connexion_etudiant')

    etudiant = Student.objects.get(id=request.session['etudiant_id'])

    # Récupérer toutes les séquences disponibles pour la filière
    sequences_dispo = Evaluation.objects.filter(
        filiere=etudiant.filiere
    ).values_list('sequence', flat=True).distinct().order_by('sequence')

    bulletins = []
    for seq in sequences_dispo:
        # Prendre la première évaluation de cette séquence comme référence
        eval_ref = Evaluation.objects.filter(
            filiere=etudiant.filiere,
            sequence=seq
        ).first()

        if eval_ref:
            bulletins.append({
                'sequence': seq,
                'eval_id': eval_ref.id,
            })

    return render(request, 'mes_bulletins.html', {
        'etudiant': etudiant,
        'bulletins': bulletins,
    })


def mes_paiements(request):
    if 'etudiant_id' not in request.session:
        return redirect('connexion_etudiant')

    etudiant = Student.objects.get(id=request.session['etudiant_id'])
    paiements = Paiement.objects.filter(
        etudiant=etudiant
    ).order_by('date_paiement')

    return render(request, 'mes_paiements.html', {
        'etudiant': etudiant,
        'paiements': paiements,
    })

