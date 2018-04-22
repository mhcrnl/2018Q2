/***************************************************************
 * Name:      wxwidgetApp.h
 * Purpose:   Defines Application Class
 * Author:    mnh ()
 * Created:   2018-04-08
 * Copyright: mnh ()
 * License:
 **************************************************************/

#ifndef WXWIDGETAPP_H
#define WXWIDGETAPP_H

#include <wx/app.h>

class wxwidgetApp : public wxApp
{
    public:
        virtual bool OnInit();
};

#endif // WXWIDGETAPP_H
