
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student
from .models import Admin
from .models import Enseignant
from .models import Filiere
from .models import Cours
from .models import Paiement
import datetime
from django.http import JsonResponse
from .models import Evaluation
from .models import Note


import hashlib

def accueil(request):
    return render(request, 'accueil.html')

def connexion_etudiant(request):
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            etudiant = Student.objects.get(email=email, password=password_hash)
            request.session['etudiant_id']  = etudiant.id
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

    return render(request, 'dashboard_admin.html', {  'active_page': 'dashboard_admin', 'nom': nom,'role':role})

def students(request):
    liste_filieres = Filiere.objects.all()  # Pour remplir le select

    if request.method == 'POST':
        nom              = request.POST.get('nom')
        prenom           = request.POST.get('prenom')
        date_naissance   = request.POST.get('date_naissance')
        sexe             = request.POST.get('sexe')
        adresse          = request.POST.get('adresse')
        telephone        = request.POST.get('telephone')
        email            = request.POST.get('email')
        password         = request.POST.get('password')
        filiere      = request.POST.get('filiere')  # ID envoyé depuis le select
        nom_parent       = request.POST.get('nom_parent')
        telephone_parent = request.POST.get('telephone_parent')
        photo            = request.FILES.get('photo')
        formation        = request.POST.get('formation')

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        filiere = Filiere.objects.get(id=filiere)

        if Student.objects.filter(email=email).exists():
            messages.error(request, 'Cet email existe déjà !')
            return redirect('etudiants')

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
        messages.success(request, 'Etudiant inscrit avec succès !')
        return redirect('etudiants')

    liste_etudiants = Student.objects.all().order_by('nom')
    return render(request, 'etudiants.html', {'etudiants': liste_etudiants, 'filieres': liste_filieres})

def dashboard_etudiant(request):
    if 'etudiant_id' not in request.session:
        return redirect('connexion_etudiant')
    etudiant = Student.objects.get(id=request.session['etudiant_id'])
    return render(request, 'dashboard_admin.html', {'etudiant': etudiant})

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
    return render(request, 'enseignants.html',{'enseignants': liste_enseignants})


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
        etudiant_id  = request.POST.get('etudiant_id')
        montant      = request.POST.get('montant_verse')
        date_paie    = request.POST.get('date_paiement')
        frais_total  = request.POST.get('frais_total')
        deja_paye    = request.POST.get('deja_paye')

        etudiant     = Student.objects.get(id=etudiant_id)

        # Calcul reste à payer
        reste = float(frais_total) - float(deja_paye) - float(montant)

        # Numéro reçu automatique
        numero = f"RECU-{datetime.datetime.now().year}-{str(Paiement.objects.count()+1).zfill(3)}"

        paiement = Paiement.objects.create(
            etudiant       = etudiant,
            montant_verse  = montant,
            date_paiement  = date_paie,
            frais_total    = frais_total,
            deja_paye      = deja_paye,
            reste_a_payer  = reste,
            numero_recu    = numero,
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
    filieres= Filiere.objects.all()
    emplois = EmploiDuTemps.objects.select_related('cours', 'enseignant', 'filiere').all()

    return render(request, 'emploi_du_temps.html', {
        "emplois": emplois,
        'cours_list': cours_list,
        'enseignants': enseignants,
        'filieres': filieres,
        'erreur': erreur

    })

def emploi_events(request):
    emplois = EmploiDuTemps.objects.select_related('cours', 'enseignant','filiere').all()
    events = []

    for emploi in emplois:
        events.append({
            'title': f"{emploi.cours.nom} - {emploi.filiere.nom }",
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
    evaluations = Evaluation.objects.all()
    etudiants = []

    filiere_id = request.GET.get("filiere")
    evaluation_id = request.GET.get("evaluation")

    # 👉 Charger étudiants selon filière
    if filiere_id:
        etudiants = Student.objects.filter(filiere_id=filiere_id)

    # 👉 Ajouter une évaluation
    if request.method == "POST" and "add_evaluation" in request.POST:
        nom = request.POST.get("nom")
        filiere = request.POST.get("filiere")
        cours_id = request.POST.get("cours")
        coefficient = request.POST.get("coefficient")


        Evaluation.objects.create(
            nom=nom,
            filiere_id=filiere,
            cours_id=cours_id,
            coefficient=coefficient,

        )

        messages.success(request, "Evaluation ajoutée")
        return redirect('evaluation_teacher')

    # 👉 Enregistrer notes
    if request.method == "POST" and "save_notes" in request.POST:
        evaluation_id = request.POST.get("evaluation_id")

        for key, value in request.POST.items():
            if key.startswith("note_") and value:
                student_id = key.split("_")[1]

                Note.objects.update_or_create(
                    etudiant_id=student_id,
                    evaluation_id=evaluation_id,
                    defaults={"note": value}
                )

        messages.success(request, "Notes enregistrées")
        return redirect('evaluation_teacher')

    return render(request, "evaluation_teacher.html", {
        "filieres": filieres,
        "cours": cours,
        "evaluations": evaluations,
        "etudiants": etudiants
    })