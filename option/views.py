from django.http import Http404
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import StrategyForm

from .models import Strategy

class StrategyListView(LoginRequiredMixin, ListView):
    model = Strategy
    template_name = 'strategy_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Strategies"
        return context
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class StrategyCreateView(CreateView):
    template_name = 'strategy_create_update.html'
    form_class = StrategyForm
    model = Strategy

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create Strategy"
        return context

    def form_valid(self, form):
        strategy = form.save(commit=False)
        strategy.user = self.request.user
        strategy.save()
        form.save_m2m()
        return super(StrategyCreateView, self).form_valid(form)

class StrategyUpdateView(UpdateView):
    template_name = 'strategy_create_update.html'
    form_class = StrategyForm
    model = Strategy

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Strategy"
        return context

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
        

strategy_list_view = StrategyListView.as_view()
strategy_create_view = StrategyCreateView.as_view()
strategy_update_view = StrategyUpdateView.as_view()
