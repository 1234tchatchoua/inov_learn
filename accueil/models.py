import random
from email.policy import default

from django.db import models


class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    duree = models.PositiveIntegerField(help_text="Durée en années")
    frais_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom


class Student(models.Model):
    # Informations personnelles
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=1)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    role = models.CharField(max_length=100, default='student')
    formation = models.CharField(max_length=255, default='DQP')

    # Filière
    filiere = models.ForeignKey(
        Filiere,
        on_delete=models.CASCADE,
        related_name='etudiants',
        null=True,
        blank=True
    )

    # Parent
    nom_parent = models.CharField(max_length=100)
    telephone_parent = models.CharField(max_length=20)

    # Date inscription auto
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Admin(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=100, default='admin')

    def __str__(self):
        return self.email


class Enseignant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=1)
    adresse = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='enseignants/', blank=True, null=True)
    role = models.CharField(max_length=100, default='teacher')


    def __str__(self):
        return f"{self.nom} {self.prenom if self.prenom else ''}".strip()

class Cours(models.Model):
    nom = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True, blank=True)
    enseignant = models.ForeignKey(
        Enseignant,
        on_delete=models.CASCADE,
        related_name='cours'
    )
    filiere = models.ForeignKey(
        Filiere,
        on_delete=models.CASCADE,
        related_name='cours'
    )

    def generer_code_unique(self):
        while True:
            numero = random.randint(1, 1000)
            code = f"CRS{numero}"
            if not Cours.objects.filter(code=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generer_code_unique()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.code})"


class Paiement(models.Model):
    etudiant = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='paiements'
    )
    montant_verse = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField()
    frais_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deja_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reste_a_payer = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    numero_recu = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.etudiant.nom} - {self.montant_verse}"


class EmploiDuTemps(models.Model):
    cours = models.ForeignKey(
        Cours,
        on_delete=models.CASCADE,
        related_name='emplois'
    )
    enseignant = models.ForeignKey(
        Enseignant,
        on_delete=models.CASCADE,
        related_name='emplois'
    )
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='emplois')
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    def __str__(self):
        return f"{self.cours.nom} - {self.filiere.nom} {self.heure_debut}"


class Evaluation(models.Model):
    nom = models.CharField(max_length=100)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    coefficient = models.FloatField()

    def __str__(self):
        return self.nom


class Note(models.Model):
    etudiant = models.ForeignKey(Student, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    note = models.FloatField()

    def __str__(self):
        return f"{self.etudiant.nom} - {self.note}"