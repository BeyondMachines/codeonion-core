from django.contrib import admin

from scanner.models import Dependency, Scanned_Repo, Repo_Dependency_Pair
# Register your models here.

class DependencyModelAdmin(admin.ModelAdmin):
    list_display = ('dependency_name', 'dependency_language', 'dependency_license', 'dependency_license_last_checked_date')

    def get_topic(self, obj):  # using this we can render the foreign key information
        return obj.dependency_name

admin.site.register(Dependency, DependencyModelAdmin)


class Scanned_RepoModelAdmin(admin.ModelAdmin):
    list_display = ('repo_name', 'repo_store', 'repo_primary_language', 'repo_last_checked_date')

    def get_topic(self, obj):  # using this we can render the foreign key information
        return obj.repo_name

admin.site.register(Scanned_Repo, Scanned_RepoModelAdmin)


class Repo_Dependency_PairModelAdmin(admin.ModelAdmin):
    list_display = ('repo', 'dependency', 'date_scanned')

    def get_topic(self, obj):  # using this we can render the foreign key information
        return obj.repo

admin.site.register(Repo_Dependency_Pair, Repo_Dependency_PairModelAdmin)