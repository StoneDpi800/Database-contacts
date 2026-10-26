import base64
import flet as ft


def main(page: ft.Page):
    page.title = "Test aperçu"

    etat = {"octets": None}

    texte = ft.Text("Aucune photo choisie")
    apercu = ft.Image(src="", width=150, height=150, fit=ft.BoxFit.COVER, visible=False)

    async def choisir(e):
        fichiers = await ft.FilePicker().pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE,
        )
        if not fichiers:
            return

        with open(fichiers[0].path, "rb") as f:
            octets = f.read()

        etat["octets"] = octets
        apercu.src = base64.b64encode(octets).decode()
        apercu.visible = True
        texte.value = f"{fichiers[0].name} - {len(octets)} octets"
        page.update()

    page.add(
        ft.Button("Choisir une photo", on_click=choisir),
        texte,
        apercu,
    )


ft.run(main)