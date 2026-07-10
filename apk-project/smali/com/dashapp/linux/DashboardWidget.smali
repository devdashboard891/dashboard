.class public Lcom/dashapp/linux/DashboardWidget;
.super Landroid/appwidget/AppWidgetProvider;
.source "DashboardWidget.java"

.method public constructor <init>()V
    .locals 0
    invoke-direct {p0}, Landroid/app/AppWidgetProvider;-><init>()V
    return-void
.end method

.method public onUpdate(Landroid/content/Context;Landroid/appwidget/AppWidgetManager;[I)V
    .locals 6

    array-length v0, p3
    if-lez v0, :cond_1

    new-instance v0, Landroid/content/Intent;
    invoke-direct {v0}, Landroid/content/Intent;-><init>()V
    const-string v1, "com.dashapp.linux"
    const-string v2, "com.dashapp.linux.MainActivity"
    invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->setClassName(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    const/high16 v1, 0x10000000
    invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    const/4 v1, 0x0
    const/high16 v2, 0x02000000
    invoke-static {p1, v1, v0, v2}, Landroid/app/PendingIntent;->getActivity(Landroid/content/Context;ILandroid/content/Intent;I)Landroid/app/PendingIntent;
    move-result-object v0

    new-instance v1, Landroid/widget/RemoteViews;
    invoke-virtual {p1}, Landroid/content/Context;->getPackageName()Ljava/lang/String;
    move-result-object v2
    const v3, 0x7f030001
    invoke-direct {v1, v2, v3}, Landroid/widget/RemoteViews;-><init>(Ljava/lang/String;I)V

    const v2, 0x7f030001
    invoke-virtual {v1, v2, v0}, Landroid/widget/RemoteViews;->setOnClickPendingIntent(ILandroid/app/PendingIntent;)V

    array-length v0, p3
    const/4 v2, 0x0
    :goto_0
    if-ge v2, v0, :cond_0
    aget v3, p3, v2
    invoke-virtual {p2, v3, v1}, Landroid/appwidget/AppWidgetManager;->updateAppWidget(ILandroid/widget/RemoteViews;)V
    add-int/lit8 v2, v2, 0x1
    goto :goto_0

    :cond_0
    :goto_1
    return-void

    :cond_1
    goto :goto_1
.end method
