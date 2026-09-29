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


class SagerSelectors:
    """Selectors til "Søg sager", fra Blue Prism objektet "Netforvaltning Sundhed
    (Chrome)". Siden kan ikke åbnes med url (404), man skal klikke sig ind via menuen."""

    # menu: hover "Sager" og klik "Søg sager" // menu: hover "Sager", click "Søg sager"
    MENU_SAGER = "#Menu1_mainMenu_0"
    MENU_SOEG_SAGER = "table#Menu1_mainMenu_9"

    # cpr søgefelt
    CPR = "#tbCpr"

    # sagsbehandler - "- Alle -" vælges, så alle sager på borgeren findes
    # // caseworker - "- Alle -" is selected so all of the citizen's cases are found
    SAGSBEHANDLER = "#ddlCaseworker"
    ALLE_SAGSBEHANDLERE = "- Alle -"

    # søgeknap
    SOEG = "#btnCaseSearch"

    # resultattabel og tom-række // result table and empty row
    SAGSTABEL = "table#gvCaseList"
    INGEN_SAGER = "tr#trEmpty"
