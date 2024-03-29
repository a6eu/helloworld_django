"""
URL configuration for site_market project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include("api_market.urls")),
    path("api/v1/", include("basket.urls")),
    path("api/v1/", include("favorites.urls")),
    path("api/v1/", include("order.urls")),
    path("api/v1/", include("products.urls")),
    path("api/v1/", include("comment.urls")),
    path("api/v1/", include("category.urls")),
    path("api/v1/", include("brand.urls")),
    path("api/v1/", include("news.urls")),
    path("api/v1/", include("demand.urls")),
    path("api/v1/auth/", include("custom_auth.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            template_name="swagger-ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


