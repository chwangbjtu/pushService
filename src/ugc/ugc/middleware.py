class DisableCSRF(object):
	def process_request(self, request):
		setattr(request, '_dont_enforce_csrf_checks', True)


class RepaireCookie(object):
    def process_request(self,request):
        if not request.POST.has_key("sessionid"):
            return None
        request.COOKIES["sessionid"] = request.POST["sessionid"]
        return None
