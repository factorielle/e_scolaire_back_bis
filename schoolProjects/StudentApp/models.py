from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('parent', 'Parent'),
        ('prof', 'Professeur'),
        ('eleve', 'Élève'),
        ('admin', 'Administrateur'),
    ]

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    adresse = models.CharField(max_length=255)
    profile_photo = models.ImageField(verbose_name='Photo de profil', default='https://www.freepik.com/premium-vector/african-american-man-face_2585211.htm#fromView=search&page=1&position=40&uuid=76e184f4-fc4d-4e05-81c9-737edda42205')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def save(self, *args, **kwargs):
        if self.password:
            self.set_password(self.password)  # hacher le mot de passe
        super().save(*args, **kwargs)




class Matiere(models.Model):
    libelle = models.CharField(max_length=100)
    coefficient = models.PositiveIntegerField()


class Note(models.Model):
    valeur = models.DecimalField(max_digits=5, decimal_places=2)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)


class Classe(models.Model):
    nom = models.CharField(max_length=100)
    effectif = models.PositiveIntegerField()


class Admission(models.Model):
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE)
    annee = models.IntegerField()


class Eleve(models.Model):
    user = models.OneToOneField(User, default='', on_delete=models.CASCADE, primary_key=True)
    classes = models.ManyToManyField(Classe, through=Admission)
    date_naissance = models.DateField()


class Parent(models.Model):
    user = models.OneToOneField(User, default='', on_delete=models.CASCADE, primary_key=True)


class Inscription(models.Model):
    parent = models.ForeignKey(Parent, default='', on_delete=models.CASCADE)
    date_inscription = models.DateField()


class Professeur(models.Model):
    user = models.OneToOneField(User, default='', on_delete=models.CASCADE, primary_key=True)
    matieres = models.ManyToManyField(Matiere)


class Enseignement(models.Model):
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)


class Admin(models.Model):
    user = models.OneToOneField(User, default='', on_delete=models.CASCADE, primary_key=True)


class Dossier(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dossiers_created')
    update_at = models.DateTimeField(auto_now=True)
    update_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dossiers_updated')


class Rapport(models.Model):
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rapports_created')
    update_at = models.DateTimeField(auto_now=True)
    update_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rapports_updated')


class Appreciation(models.Model):
    rapport = models.ForeignKey(Rapport, on_delete=models.CASCADE)
    texte = models.TextField()


class Bulletin(models.Model):
    user = models.OneToOneField(User, default='', on_delete=models.CASCADE, primary_key=True)
    notes = models.ManyToManyField(Note, through='BulletinNote')
    commentaires = models.TextField(default='')
    date_generation = models.DateField(default='')


class BulletinNote(models.Model):
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
