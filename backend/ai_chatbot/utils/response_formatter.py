class ResponseFormatter:
    @staticmethod
    def format_response(response, response_type):
        if response_type == 'cbt':
            return f"CBT Intervention: {response}"
        elif response_type == 'mindfulness':
            return f"Mindfulness Exercise: {response}"
        elif response_type == 'crisis':
            return f"Crisis Support: {response}"
        else:
            return response