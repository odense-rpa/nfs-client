def nav():
    pass


class NFSSelectors:
    """Selector constants used by the Playwright client."""

    # tilpasning
    TILPASNING = "text=Tilpasning"

    # kommunens brugere - liste over brugere
    KOMMUNENS_BRUGERE = "text=Kommunens brugere"

    # email søgefelt
    EMAIL_SØGEFELT = "#muniUsers_TextBox2"

    # email søgeknap
    EMAIL_SØGEKNAP = "#muniUsers_Button1"

    # liste over brugere - skal finde den række hvor email kolonnen matcher præcist og klikke på detaljer for den bruger
    LISTE_OVER_BRUGERE = "#muniUsers_UserGridView1_dgGrid"

    # række i listen over brugere
    BRUGER_RÆKKE = "#muniUsers_UserGridView1_dgGrid > tbody > tr"

    # email kolonne i listen over brugere
    EMAIL_KOLONNE = "td:nth-child(2)"

    # rolle kolonne i listen over brugere
    ROLLE_KOLONNE = "td:nth-child(3)"
    
    # detaljer for bruger
    DETALJER_FOR_BRUGER = "#muniUsers_UserGridView1_dgGrid > tbody > tr:nth-child(2) > td:nth-child(5) > a"
    #"a:has-text('Detaljer')"

    DETALJER_FOR_BRUGERE = DETALJER_FOR_BRUGER
    #Ved ikke hvorfor der er flertal, det var ai der kom med det

    # slet bruger knap
    SLET_BRUGER_KNAP = "#EditUserSettings2_btnDelete"

    #ok knap ved sletning
    #I really dont know...
