def nav():
    pass


class NFSSelectors:
    """Selector constants used by the Playwright client."""

    # ----------------------------------- iframe & nested content --------------------------------

    # iframe
    IFRAME = "iframe#frameset"

    # iframe content
    IFRAME_CONTENT = "#frameContent"

    # form inde i iframe
    FORM = "form#Form1"

    # --------------------------------------- Navigering -----------------------------------------

    # tilpasning
    TILPASNING = "text=Tilpasning"

    # kommunens brugere - liste over brugere
    KOMMUNENS_BRUGERE = "text=Kommunens brugere"

    # detaljer for bruger
    DETALJER_FOR_BRUGER = "td:nth-child(5) a"

    # icon/billede link til forside
    FORSIDE_LINK = "#IMG1"

    # -------------------------------- Email søgning og resultat ---------------------------------

    # email søgefelt
    EMAIL_SØGEFELT = "#muniUsers_TextBox2"

    # email søgeknap
    EMAIL_SØGEKNAP = "#muniUsers_Button1"

    # liste over brugere
    LISTE_OVER_BRUGERE = "#muniUsers_UserGridView1_dgGrid"

    # generel bruger række i listen over brugere
    BRUGER_RÆKKE = "#muniUsers_UserGridView1_dgGrid > tbody > tr"

    # specifik bruger række i liste over brugere - bruges til at tjekke om bruger er slettet
    RESULTAT_I_LISTE_OVER_BRUGER = (
        "#muniUsers_UserGridView1_dgGrid > tbody > tr:nth-child(2)"
    )

    # email kolonne i listen over brugere
    EMAIL_KOLONNE = "td:nth-child(2)"

    # rolle kolonne i listen over brugere
    ROLLE_KOLONNE = "td:nth-child(3)"

    # ------------------------------------------ Slet --------------------------------------------

    # slet bruger knap
    SLET_BRUGER_KNAP = "#EditUserSettings2_btnDelete"
