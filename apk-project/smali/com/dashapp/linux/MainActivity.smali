.class public Lcom/dashapp/linux/MainActivity;
.super Landroid/app/Activity;
.source "MainActivity.java"

.field private webView:Landroid/webkit/WebView;
.field private offlineLoaded:Z

.method public constructor <init>()V
    .locals 1
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V
    const/4 v0, 0x0
    iput-boolean v0, p0, Lcom/dashapp/linux/MainActivity;->offlineLoaded:Z
    return-void
.end method

.method public isOfflineLoaded()Z
    .locals 1
    iget-boolean v0, p0, Lcom/dashapp/linux/MainActivity;->offlineLoaded:Z
    return v0
.end method

.method public setOfflineLoaded()V
    .locals 1
    const/4 v0, 0x1
    iput-boolean v0, p0, Lcom/dashapp/linux/MainActivity;->offlineLoaded:Z
    return-void
.end method

.method public onCreate(Landroid/os/Bundle;)V
    .locals 4

    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    const-string v0, "MainActivity"
    const-string v1, "Dashboard is starting..."
    invoke-static {v0, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    new-instance v0, Landroid/webkit/WebView;
    invoke-direct {v0, p0}, Landroid/webkit/WebView;-><init>(Landroid/content/Context;)V
    iput-object v0, p0, Lcom/dashapp/linux/MainActivity;->webView:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->getSettings()Landroid/webkit/WebSettings;
    move-result-object v1
    const/4 v2, 0x1
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setJavaScriptEnabled(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setDomStorageEnabled(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setAllowFileAccess(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setAllowFileAccessFromFileURLs(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setAllowUniversalAccessFromFileURLs(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setGeolocationEnabled(Z)V

    new-instance v1, Lcom/dashapp/linux/DashboardWebClient;
    invoke-direct {v1, p0}, Lcom/dashapp/linux/DashboardWebClient;-><init>(Lcom/dashapp/linux/MainActivity;)V
    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->setWebViewClient(Landroid/webkit/WebViewClient;)V

    new-instance v1, Lcom/dashapp/linux/DashboardChromeClient;
    invoke-direct {v1, p0}, Lcom/dashapp/linux/DashboardChromeClient;-><init>(Lcom/dashapp/linux/MainActivity;)V
    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->setWebChromeClient(Landroid/webkit/WebChromeClient;)V

    invoke-virtual {p0, v0}, Landroid/app/Activity;->setContentView(Landroid/view/View;)V

    const-string v1, "file:///android_asset/index.html"
    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;)V

    return-void
.end method
