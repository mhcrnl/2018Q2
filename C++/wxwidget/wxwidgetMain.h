/***************************************************************
 * Name:      wxwidgetMain.h
 * Purpose:   Defines Application Frame
 * Author:    mnh ()
 * Created:   2018-04-08
 * Copyright: mnh ()
 * License:
 **************************************************************/

#ifndef WXWIDGETMAIN_H
#define WXWIDGETMAIN_H

//(*Headers(wxwidgetDialog)
#include <wx/sizer.h>
#include <wx/stattext.h>
#include <wx/statline.h>
#include <wx/button.h>
#include <wx/dialog.h>
//*)

class wxwidgetDialog: public wxDialog
{
    public:

        wxwidgetDialog(wxWindow* parent,wxWindowID id = -1);
        virtual ~wxwidgetDialog();

    private:

        //(*Handlers(wxwidgetDialog)
        void OnQuit(wxCommandEvent& event);
        void OnAbout(wxCommandEvent& event);
        //*)

        //(*Identifiers(wxwidgetDialog)
        static const long ID_STATICTEXT1;
        static const long ID_BUTTON1;
        static const long ID_STATICLINE1;
        static const long ID_BUTTON2;
        //*)

        //(*Declarations(wxwidgetDialog)
        wxButton* Button1;
        wxStaticText* StaticText1;
        wxBoxSizer* BoxSizer2;
        wxButton* Button2;
        wxStaticLine* StaticLine1;
        wxBoxSizer* BoxSizer1;
        //*)

        DECLARE_EVENT_TABLE()
};

#endif // WXWIDGETMAIN_H
    