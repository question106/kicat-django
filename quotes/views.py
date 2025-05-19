from django.views.generic import ListView, CreateView, View
from django.http import JsonResponse, HttpResponseRedirect
from .models import Quote, ServiceType, ServiceCategory

class QuoteListView(ListView):
    http_method_names = ["get"]
    template_name = 'quotes/quote_list.html'
    model = Quote
    context_object_name = 'quotes'
    queryset = Quote.objects.all().order_by('-created_at')
    
class CreateQuoteView(CreateView):
    template_name = 'quotes/quote_request.html'
    http_method_names = ["get", "post"]
    model = Quote
    fields = ['name', 'company', 'email', 'phone', 'service_type', 'message', 'file', 'google_drive_link']
    success_url = "/"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_categories'] = ServiceCategory.objects.all()
        context['service_types'] = ServiceType.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            
            # Get service_type from POST data
            service_type_id = data.get('service_type')
            if not service_type_id:
                return JsonResponse({"status": "error", "message": "Service type is required"}, status=400)
            
            try:
                service_type = ServiceType.objects.get(id=service_type_id)
            except ServiceType.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Invalid service type"}, status=400)
            
            # Create the Quote object with correct fields
            quote = Quote(
                name=data.get('name', ''),
                company=data.get('company', ''),
                email=data.get('email', ''),
                phone=data.get('phone', ''),
                service_type=service_type,
                message=data.get('message', ''),
                google_drive_link=data.get('google_drive_link', '')
            )
            
            # Handle file if present
            if 'file' in request.FILES:
                quote.file = request.FILES['file']
                
            quote.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            print(str(e))  # For debugging
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

# Add this new view
class GetServiceTypesView(View):
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        if not category_id:
            return JsonResponse({
                'success': False,
                'service_types': []
            })
        
        try:
            service_types = ServiceType.objects.filter(
                category_id=category_id,
                is_active=True
            ).values('id', 'name')
            
            return JsonResponse({
                'success': True,
                'service_types': list(service_types)
            })
        except Exception as e:
            print(str(e))
            return JsonResponse({
                'success': False,
                'service_types': []
            })