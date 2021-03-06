/***************************************************************
 * Name:      wxwidgetApp.cpp
 * Purpose:   Code for Application Class
 * Author:    mnh ()
 * Created:   2018-04-08
 * Copyright: mnh ()
 * License:
 **************************************************************/

#include "wxwidgetApp.h"

//(*AppHeaders
#include "wxwidgetMain.h"
#include <wx/image.h>
//*)

IMPLEMENT_APP(wxwidgetApp);

bool wxwidgetApp::OnInit()
{
    //(*AppInitialize
    bool wxsOK = true;
    wxInitAllImageHandlers();
    if ( wxsOK )
    {
    	wxwidgetDialog Dlg(0);
    	SetTopWindow(&Dlg);
    	Dlg.ShowModal();
    	wxsOK = false;
    }
    //*)
    return wxsOK;

}
        