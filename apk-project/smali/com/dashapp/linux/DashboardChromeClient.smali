.class Lcom/dashapp/linux/DashboardChromeClient;
.super Landroid/webkit/WebChromeClient;
.source "MainActivity.java"

.field private activity:Lcom/dashapp/linux/MainActivity;

.method public constructor <init>(Lcom/dashapp/linux/MainActivity;)V
    .locals 0
    invoke-direct {p0}, Landroid/webkit/WebChromeClient;-><init>()V
    iput-object p1, p0, Lcom/dashapp/linux/DashboardChromeClient;->activity:Lcom/dashapp/linux/MainActivity;
    return-void
.end method

.method public onGeolocationPermissionsShowPrompt(Ljava/lang/String;Landroid/webkit/GeolocationPermissions$Callback;)V
    .locals 3
    const/4 v0, 0x1
    const/4 v1, 0x0
    invoke-interface {p2, p1, v0, v1}, Landroid/webkit/GeolocationPermissions$Callback;->invoke(Ljava/lang/String;ZZ)V
    return-void
.end method