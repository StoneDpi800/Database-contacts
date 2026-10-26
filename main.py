import flet as ft
import database
import asyncio
import base64
import datetime




def page_accueil(page: ft.Page):

    titre_formulaire = ft.Text("Nouveaux contact:", size=20, weight=ft.FontWeight.BOLD)
    champs_nom = ft.TextField(label="Entrer votre nom")
    champs_prenom = ft.TextField(label="Entrer votre prenom")
    champs_age = ft.TextField(label="Entrer votre age")
    champs_adresse = ft.TextField(label="Entrer votre adresse")
    champs_code_postal = ft.TextField(label="Entrer votre code postal")
    champs_ville = ft.TextField(label="Entrer votre ville")

    champs_nom_modif = ft.TextField(label="Nom")
    champs_prenom_modif = ft.TextField(label="Prenom")
    champs_age_modif = ft.TextField(label="Age")
    champs_adresse_modif = ft.TextField(label="Adresse")
    champs_code_postal_modif = ft.TextField(label="Code postal")
    champs_ville_modif = ft.TextField(label="Ville")

    ligne_nom = ft.Row(controls=[ft.Text("Nom :", width=100), champs_nom])
    ligne_prenom = ft.Row(controls=[ft.Text("Prenom :", width=100), champs_prenom])
    ligne_age = ft.Row(controls=[ft.Text("Age :", width=100), champs_age])
    ligne_adresse = ft.Row(controls=[ft.Text("Adresse :", width=100), champs_adresse])
    ligne_code_postal = ft.Row(controls=[ft.Text("Code Postal :", width=100), champs_code_postal])
    ligne_ville = ft.Row(controls=[ft.Text("Ville :", width=100), champs_ville])

    message = ft.Text("")
    ligne_message = ft.Row(controls=[ft.Text("", width=100), message])

    content_image = ft.Image(src="", width=250, height=250, fit=ft.BoxFit.COVER, visible=False)

    icon_person = ft.Icon(ft.Icons.PERSON, color=ft.Colors.GREY_600, size=125)
    cadre_image = ft.Container(width=250, height=250, bgcolor=ft.Colors.GREY_300, border_radius=10, alignment=ft.Alignment.CENTER,
                               content=icon_person)


    image_octets = {"octets": None}

    async def ouvrir_fichier(e):
            image = await ft.FilePicker().pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)
            if not image:
                return

            with open(image[0].path, "rb") as file:
                octets = file.read()

            image_octets["octets"] = octets

            content_image.src = base64.b64encode(octets).decode()
            content_image.visible = True
            cadre_image.content = content_image
            page.update()




    button_image = ft.Button("Choisir une photo", on_click=ouvrir_fichier)

    zone_photo = ft.Column(controls=[cadre_image, button_image], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)

    async def affiche_message(phrase, couleur):
        message.value = phrase
        message.color = couleur
        page.update()
        await asyncio.sleep(3)
        message.value = ""
        page.update()


    def f_ajouter(e):
        nom = champs_nom.value
        prenom = champs_prenom.value
        age = champs_age.value
        adresse = champs_adresse.value
        code_postal = champs_code_postal.value
        ville = champs_ville.value

        if not nom.strip() or not prenom.strip():
            page.run_task(affiche_message, "Le nom ou le prenom ne doivent pas etre vide !", ft.Colors.RED)
            return

        if age.isdigit() == False or not age.strip():
            page.run_task(affiche_message, "L'age doit contenire des chiffres !", ft.Colors.RED)
            return

        if not adresse.strip():
            page.run_task(affiche_message, "L'adresse ne doit pas etre vide !", ft.Colors.RED)
            return

        if not code_postal.strip():
            page.run_task(affiche_message, "Le code postal ne doit pas etre vide !", ft.Colors.RED)
            return

        if not ville.strip():
            page.run_task(affiche_message, "La ville ne doit pas etre vide !", ft.Colors.RED)
            return


        database.ajouter(nom, prenom, int(age), adresse, code_postal, ville, image_octets["octets"])
        page.run_task(affiche_message, "Contacts ajouter !", ft.Colors.GREEN)
        date_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        database.ajoute_historique(date_now, "contact ajouter", f"{nom} {prenom}")
        afficher_contacts()
        afficher_historique()
        champs_nom.value = ""
        champs_prenom.value = ""
        champs_age.value = ""
        champs_adresse.value = ""
        champs_code_postal.value = ""
        champs_ville.value = ""
        content_image.src = ""
        content_image.visible = False
        cadre_image.content = icon_person
        image_octets["octets"] = None

        page.update()




    button_ajouter = ft.Button("Ajouter", width=200, on_click=f_ajouter, tooltip="Ajouter à la liste des contacts")
    ligne_button = ft.Row(controls=[ft.Text("", width=150), button_ajouter])

    colonne_contacts = ft.Column(controls=[], scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)

    titre_liste_contacts = ft.Text("Liste des contacts:", size=18, weight=ft.FontWeight.BOLD)


    def supp_historique(e):
        database.supprimer_historique_all()
        afficher_historique()
        page.update()

    titre_historique = ft.Text("Historique", size=22, weight=ft.FontWeight.BOLD)
    button_supprime_historique = ft.IconButton(icon=ft.Icons.DELETE, tooltip="Supprimer toutes les historiques", on_click=supp_historique)
    ligne_titre_historique = ft.Row(controls=[titre_historique, button_supprime_historique], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    liste_historique = ft.Column(controls=[], spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)

    historique = ft.Container(width=400, height=350, border=ft.Border.all(1, ft.Colors.GREY_700), border_radius=10, padding=15,
        content=ft.Column(
            controls=[
                ligne_titre_historique,
                ft.Divider(),
                liste_historique
            ],
            spacing=10,
            expand=True))


    def afficher_historique():
        liste_historique.controls.clear()
        if not database.lire_historique():
            return

        for action in database.lire_historique():
            infos = ft.Text(f"{action[1]}: {action[2]} - {action[3]}", size=15)

            ligne = ft.Container(content=ft.Row(controls=[infos], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=10,
                border=ft.Border.all(1, ft.Colors.GREY_700),
                border_radius=8)

            liste_historique.controls.append(ligne)

        page.update()





    def fermer_boite_supp(e):
        page.pop_dialog()


    def confirmation_ouvrir(id_contact, nom, prenom):

        def supp(e):
            database.supprimer(id_contact)
            date_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            database.ajoute_historique(date_now, "contact supprimer", f"{nom} {prenom}")
            fermer_boite_supp(e)
            afficher_contacts()
            afficher_historique()
            page.update()

        boite_supp = ft.AlertDialog(modal=True, title=ft.Text("Confirmation de la suppression"), content=ft.Text("Voulez-vous vraiment supprimer ce contact ?"),
                                    actions=[ft.TextButton("Oui", on_click=supp), ft.TextButton("Non", on_click=fermer_boite_supp)])

        page.show_dialog(boite_supp)



    def fermer_boite_modif(e):
        page.pop_dialog()

    def ouvrir_modification(nom, prenom, age, adresse, cp, ville, id, photo=None):
        champs_nom_modif.value = nom
        champs_prenom_modif.value = prenom
        champs_age_modif.value = age
        champs_adresse_modif.value = adresse
        champs_code_postal_modif.value = cp
        champs_ville_modif.value = ville

        photo_new = {"octets": photo}

        async def ouvrir_fichier_modif(e):
            image = await ft.FilePicker().pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)
            if not image:
                return

            with open(image[0].path, "rb") as file:
                octets = file.read()

            photo_new["octets"] = octets

            photo_modif.content = ft.Image(src=base64.b64encode(octets).decode(), fit=ft.BoxFit.COVER, width=120, height=120)
            page.update()

        button_image_modif = ft.Button("Choisir une photo", on_click=ouvrir_fichier_modif)

        ligne_button_modif = ft.Row(controls=[button_image_modif], alignment=ft.MainAxisAlignment.CENTER)

        message_modif = ft.Text("", height=20)

        async def affiche_message_modif(phrase, couleur):
            message_modif.value = phrase
            message_modif.color = couleur
            page.update()
            await asyncio.sleep(3)
            message_modif.value = ""
            page.update()



        def enreg_modification(e):
            if not champs_nom_modif.value.strip() or not champs_prenom_modif.value.strip():
                page.run_task(affiche_message_modif, "Le nom ou le prenom ne doivent pas etre vide !", ft.Colors.RED)
                return
            if str(champs_age_modif.value).isdigit() == False or not str(champs_age_modif.value).strip():
                page.run_task(affiche_message_modif, "L'age doit contenire des chiffres !", ft.Colors.RED)
                return
            if not champs_adresse_modif.value.strip():
                page.run_task(affiche_message_modif, "L'adresse ne doit pas etre vide !", ft.Colors.RED)
                return
            if not champs_code_postal_modif.value.strip():
                page.run_task(affiche_message_modif, "Le code postal ne doit pas etre vide !", ft.Colors.RED)
                return
            if not champs_ville_modif.value.strip():
                page.run_task(affiche_message_modif, "La ville ne doit pas etre vide !", ft.Colors.RED)
                return

            database.modifier(id, champs_nom_modif.value, champs_prenom_modif.value, champs_age_modif.value, champs_adresse_modif.value, champs_code_postal_modif.value, champs_ville_modif.value, photo_new["octets"])
            date_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            database.ajoute_historique(date_now, "contact modifier", f"{nom} {prenom}")
            fermer_boite_modif(e)
            afficher_contacts()
            afficher_historique()
            page.update()



        if photo:
            photo_modif = ft.Container(
                width=120,
                height=120,
                bgcolor=ft.Colors.GREY_300,
                border_radius=8,
                alignment=ft.Alignment.CENTER,
                content=ft.Image(src=base64.b64encode(photo).decode(), fit=ft.BoxFit.COVER, width=120, height=120))
        else:
            photo_modif = ft.Container(
                width=120,
                height=120,
                bgcolor=ft.Colors.GREY_300,
                border_radius=8,
                alignment=ft.Alignment.CENTER,
                content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.GREY_600, size=60))

        ligne_photo_modif = ft.Row(controls=[photo_modif], alignment=ft.MainAxisAlignment.CENTER)


        boite_modif = ft.AlertDialog(
            modal=True,
            title=ft.Text("Modifier le contact", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                width=400,
                content=ft.Column(
                    controls=[
                        champs_nom_modif,
                        champs_prenom_modif,
                        champs_age_modif,
                        champs_adresse_modif,
                        champs_code_postal_modif,
                        champs_ville_modif,
                        message_modif,
                        ligne_photo_modif,
                        ligne_button_modif],
                    tight=True,
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO)),
            actions=[
                ft.Button("Enregistrer", on_click=enreg_modification),
                ft.TextButton("Annuler", on_click=fermer_boite_modif)])

        page.show_dialog(boite_modif)





    def afficher_contacts():
        colonne_contacts.controls.clear()
        rouge = ft.TextStyle(color=ft.Colors.RED)

        if not database.lire_tous():
            colonne_contacts.controls.append(
                ft.Container(
                    content=ft.Text("Aucun contact", size=28, weight=ft.FontWeight.BOLD),
                    alignment=ft.Alignment.CENTER,
                    expand=True))
            return

        for contact in database.lire_tous():
            if contact[7]:
                photo = ft.Image(
                    src=base64.b64encode(contact[7]).decode(),
                    width=80,
                    height=80,
                    fit=ft.BoxFit.COVER,
                    border_radius=8)
            else:
                photo = ft.Container(
                    width=80,
                    height=80,
                    bgcolor=ft.Colors.GREY_300,
                    border_radius=8,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.GREY_600, size=40))

            infos = ft.Text(
                size=16,
                expand=True,
                spans=[
                    ft.TextSpan("Id: ", style=rouge),
                    ft.TextSpan(f"{contact[0]} | "),
                    ft.TextSpan("Nom: ", style=rouge),
                    ft.TextSpan(f"{contact[1]} | "),
                    ft.TextSpan("Prenom: ", style=rouge),
                    ft.TextSpan(f"{contact[2]} | "),
                    ft.TextSpan("Age: ", style=rouge),
                    ft.TextSpan(f"{contact[3]} ans | "),
                    ft.TextSpan("Adresse: ", style=rouge),
                    ft.TextSpan(f"{contact[4]} | "),
                    ft.TextSpan("Code postal: ", style=rouge),
                    ft.TextSpan(f"{contact[5]} | "),
                    ft.TextSpan("Ville: ", style=rouge),
                    ft.TextSpan(f"{contact[6]}"),
                ],
            )

            bouton_modifier = ft.IconButton(icon=ft.Icons.EDIT, tooltip="Modifier", on_click=lambda e, c=contact: ouvrir_modification(c[1], c[2], c[3], c[4], c[5], c[6], c[0], c[7]))
            bouton_supprimer = ft.IconButton(icon=ft.Icons.DELETE, tooltip="Supprimer", on_click=lambda e, c=contact: confirmation_ouvrir(c[0], c[1], c[2]))

            ligne = ft.Container(
                content=ft.Row(
                    controls=[photo, infos, bouton_modifier, bouton_supprimer],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=10,
                border=ft.Border.all(1, ft.Colors.GREY_700),
                border_radius=8,
            )
            colonne_contacts.controls.append(ligne)
        page.update()


    def recherche(barre_recherche):
        colonne_contacts.controls.clear()
        rouge = ft.TextStyle(color=ft.Colors.RED)
        for contact in database.lire_tous():
            if barre_recherche.value.lower() in contact[1].lower():
                if contact[7]:
                    photo = ft.Image(
                        src=base64.b64encode(contact[7]).decode(),
                        width=80,
                        height=80,
                        fit=ft.BoxFit.COVER,
                        border_radius=8)
                else:
                    photo = ft.Container(
                        width=80,
                        height=80,
                        bgcolor=ft.Colors.GREY_300,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.GREY_600, size=40))

                infos = ft.Text(
                    size=16,
                    expand=True,
                    spans=[
                        ft.TextSpan("Id: ", style=rouge),
                        ft.TextSpan(f"{contact[0]} | "),
                        ft.TextSpan("Nom: ", style=rouge),
                        ft.TextSpan(f"{contact[1]} | "),
                        ft.TextSpan("Prenom: ", style=rouge),
                        ft.TextSpan(f"{contact[2]} | "),
                        ft.TextSpan("Age: ", style=rouge),
                        ft.TextSpan(f"{contact[3]} ans | "),
                        ft.TextSpan("Adresse: ", style=rouge),
                        ft.TextSpan(f"{contact[4]} | "),
                        ft.TextSpan("Code postal: ", style=rouge),
                        ft.TextSpan(f"{contact[5]} | "),
                        ft.TextSpan("Ville: ", style=rouge),
                        ft.TextSpan(f"{contact[6]}"),
                    ],
                )

                bouton_modifier = ft.IconButton(icon=ft.Icons.EDIT, tooltip="Modifier",
                                                on_click=lambda e, c=contact: ouvrir_modification(c[1], c[2], c[3],c[4], c[5], c[6],c[0], c[7]))
                bouton_supprimer = ft.IconButton(icon=ft.Icons.DELETE, tooltip="Supprimer",
                                                 on_click=lambda e, c=contact: confirmation_ouvrir(c[0]))

                ligne = ft.Container(
                    content=ft.Row(
                        controls=[photo, infos, bouton_modifier, bouton_supprimer],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=10,
                    border=ft.Border.all(1, ft.Colors.GREY_700),
                    border_radius=8,
                )
                colonne_contacts.controls.append(ligne)
        page.update()



    barre_recherche = ft.SearchBar(bar_hint_text="Entrer un nom de famille", width=500, bar_leading=ft.Icon(ft.Icons.SEARCH), on_change=lambda e: recherche(barre_recherche))

    ligne_title_recherche = ft.Row(controls=[titre_liste_contacts, barre_recherche], spacing=40)



    def change_fond(button):
        if button.icon == ft.Icons.BEDTIME_OUTLINED:
            page.theme_mode = ft.ThemeMode.LIGHT
            button.icon = ft.Icons.BEDTIME_OFF_OUTLINED
        elif button.icon == ft.Icons.BEDTIME_OFF_OUTLINED:
            page.theme_mode = ft.ThemeMode.DARK
            button.icon = ft.Icons.BEDTIME_OUTLINED

        page.update()


    button_change_fond = ft.IconButton(icon=ft.Icons.BEDTIME_OUTLINED, on_click=lambda e: change_fond(button_change_fond))

    ligne_haut = ft.Row(controls=[titre_formulaire, button_change_fond], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)


    colonne_champs = ft.Column(controls=[ligne_nom, ligne_prenom, ligne_age, ligne_adresse, ligne_code_postal, ligne_ville])

    ligne_formulaire = ft.Row(
        controls=[
            colonne_champs,
            zone_photo,
            historique
        ],
        spacing=200,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    page.add(ligne_haut)
    page.add(ligne_formulaire)
    page.add(ligne_message)
    page.add(ligne_button)
    page.add(ft.Divider(), ligne_title_recherche, colonne_contacts)

    afficher_contacts()
    afficher_historique()




def main(page: ft.Page):
    page.title = "Gestion des contacts"
    page.window.width = 1080
    page.window.height = 800


    page_accueil(page)


ft.run(main)