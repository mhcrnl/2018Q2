#include <sdk.h> // Code::Blocks SDK
#include <configurationpanel.h>
#include <logmanager.h>
#include "Salut.h"

// Register the plugin with Code::Blocks.
// We are using an anonymous namespace so we don't litter the global one.
namespace
{
    PluginRegistrant<Salut> reg(_T("Salut"));
}

// constructor
Salut::Salut()
{
    // Make sure our resources are available.
    // In the generated boilerplate code we have no resources but when
    // we add some, it will be nice that this code is in place already ;)
    if(!Manager::LoadResource(_T("Salut.zip")))
    {
        NotifyMissingFile(_T("Salut.zip"));
    }
}

// destructor
Salut::~Salut()
{
}

void Salut::OnAttach()
{
    // do whatever initialization you need for your plugin
    // NOTE: after this function, the inherited member variable
    // m_IsAttached will be TRUE...
    // You should check for it in other functions, because if it
    // is FALSE, it means that the application did *not* "load"
    // (see: does not need) this plugin...
}

void Salut::OnRelease(bool appShutDown)
{
    // do de-initialization for your plugin
    // if appShutDown is true, the plugin is unloaded because Code::Blocks is being shut down,
    // which means you must not use any of the SDK Managers
    // NOTE: after this function, the inherited member variable
    // m_IsAttached will be FALSE...
}

int Salut::Execute()
{
    // do your magic ;)
    //NotImplemented(_T("Salut::Execute()"));
    if(!IsAttached())
     return -1;
    Manager::Get()->GetLogManager()->Log(_("Salut!"));
    return 0;
}
