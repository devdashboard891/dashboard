.class Lcom/dashapp/linux/DashboardWebClient;
.super Landroid/webkit/WebViewClient;
.source "MainActivity.java"

.field private activity:Lcom/dashapp/linux/MainActivity;

.method public constructor <init>(Lcom/dashapp/linux/MainActivity;)V
    .locals 0
    invoke-direct {p0}, Landroid/webkit/WebViewClient;-><init>()V
    iput-object p1, p0, Lcom/dashapp/linux/DashboardWebClient;->activity:Lcom/dashapp/linux/MainActivity;
    return-void
.end method

.method public onReceivedError(Landroid/webkit/WebView;ILjava/lang/String;Ljava/lang/String;)V
    .locals 2
    iget-object v0, p0, Lcom/dashapp/linux/DashboardWebClient;->activity:Lcom/dashapp/linux/MainActivity;
    invoke-virtual {v0}, Lcom/dashapp/linux/MainActivity;->isOfflineLoaded()Z
    move-result v0
    if-nez v0, :cond_0
    iget-object v0, p0, Lcom/dashapp/linux/DashboardWebClient;->activity:Lcom/dashapp/linux/MainActivity;
    invoke-virtual {v0}, Lcom/dashapp/linux/MainActivity;->setOfflineLoaded()V
    const-string v0, "file:///android_asset/index.html"
    invoke-virtual {p1, v0}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;)V
    :cond_0
    return-void
.end method

.method public shouldOverrideUrlLoading(Landroid/webkit/WebView;Landroid/webkit/WebResourceRequest;)Z
    .locals 3
    .annotation build Landroid/annotation/TargetApi;
        value = 0x15
    .end annotation

    invoke-interface {p2}, Landroid/webkit/WebResourceRequest;->getUrl()Landroid/net/Uri;
    move-result-object v0
    invoke-virtual {v0}, Landroid/net/Uri;->toString()Ljava/lang/String;
    move-result-object v0

    const-string v1, "file://"
    invoke-virtual {v0, v1}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z
    move-result v1
    if-eqz v1, :cond_0
    const/4 v0, 0x0
    return v0

    :cond_0
    const-string v1, "about:blank"
    invoke-virtual {v0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v1
    if-eqz v1, :cond_1
    const/4 v0, 0x0
    return v0

    :cond_1
    new-instance v1, Landroid/content/Intent;
    const-string v2, "android.intent.action.VIEW"
    invoke-direct {v1, v2}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V
    invoke-interface {p2}, Landroid/webkit/WebResourceRequest;->getUrl()Landroid/net/Uri;
    move-result-object p2
    invoke-virtual {v1, p2}, Landroid/content/Intent;->setData(Landroid/net/Uri;)Landroid/content/Intent;
    iget-object p2, p0, Lcom/dashapp/linux/DashboardWebClient;->activity:Lcom/dashapp/linux/MainActivity;
    invoke-virtual {p2, v1}, Lcom/dashapp/linux/MainActivity;->startActivity(Landroid/content/Intent;)V
    const/4 p2, 0x1
    return p2
.end method

.method public shouldOverrideUrlLoading(Landroid/webkit/WebView;Ljava/lang/String;)Z
    .locals 3

    const-string v0, "file://"
    invoke-virtual {p2, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z
    move-result v0
    if-eqz v0, :cond_0
    const/4 p1, 0x0
    return p1

    :cond_0
    const-string v0, "about:blank"
    invoke-virtual {p2, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v0
    if-eqz v0, :cond_1
    const/4 p1, 0x0
    return p1

    :cond_1
    new-instance v0, Landroid/content/Intent;
    const-string v1, "android.intent.action.VIEW"
    invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V
    invoke-static {p2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;
    move-result-object p2
    invoke-virtual {v0, p2}, Landroid/content/Intent;->setData(Landroid/net/Uri;)Landroid/content/Intent;
    iget-object p2, p0, Lcom/dashapp/linux/DashboardWebClient;->activity:Lcom/dashapp/linux/MainActivity;
    invoke-virtual {p2, v0}, Lcom/dashapp/linux/MainActivity;->startActivity(Landroid/content/Intent;)V
    const/4 p2, 0x1
    return p2
.end method