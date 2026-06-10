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


    # -------------------------------- Email søgning og resultat ---------------------------------

    # email søgefelt
    EMAIL_SØGEFELT = "#muniUsers_TextBox2"

    # email søgeknap
    EMAIL_SØGEKNAP = "#muniUsers_Button1"

    # liste over brugere
    LISTE_OVER_BRUGERE = "#muniUsers_UserGridView1_dgGrid"

    # række i listen over brugere
    BRUGER_RÆKKE = "#muniUsers_UserGridView1_dgGrid > tbody > tr"

    # email kolonne i listen over brugere
    EMAIL_KOLONNE = "td:nth-child(2)"

    # rolle kolonne i listen over brugere
    ROLLE_KOLONNE = "td:nth-child(3)"

    
    # ------------------------------------------ Slet --------------------------------------------

    # slet bruger knap
    SLET_BRUGER_KNAP = "#EditUserSettings2_btnDelete"

    #ok knap ved sletning
    #I really dont know...