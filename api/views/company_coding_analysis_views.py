from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.coding_platform_models import Employee, LeetCodeAnalysisHistory
from api.services.leetcode_service import LeetCodeService
from django.http import HttpResponse
import csv
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CompanyLeetCodeAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Analyze a list of LeetCode usernames.
        """
        try:
            usernames = []
            
            # Handle manual URLs/Usernames input
            urls_text = request.data.get('urls', '')
            if urls_text:
                # Split by newline or comma and clean up
                for line in urls_text.replace(',', '\n').split('\n'):
                    line = line.strip()
                    if line:
                        # Extract username from URL if needed (simple logic: take last part)
                        # e.g. https://leetcode.com/u/username/ -> username
                        # e.g. https://leetcode.com/username -> username
                        parts = [p for p in line.split('/') if p]
                        if parts:
                            usernames.append(parts[-1])
            
            # Handle CSV file upload
            csv_file = request.FILES.get('csv_file')
            if csv_file:
                try:
                    decoded_file = csv_file.read().decode('utf-8').splitlines()
                    reader = csv.reader(decoded_file)
                    for row in reader:
                        if row:
                            # Assume first column is username/url
                            line = row[0].strip()
                            if line:
                                parts = [p for p in line.split('/') if p]
                                if parts:
                                    usernames.append(parts[-1])
                except Exception as e:
                    return Response({'error': f'Error reading CSV: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

            # Deduplicate
            usernames = list(set(usernames))

            if not usernames:
                return Response({'error': 'No usernames provided'}, status=status.HTTP_400_BAD_REQUEST)

            results = []
            for username in usernames:
                try:
                    stats = LeetCodeService.get_user_stats(username)
                    if stats:
                        results.append({
                            'username': username,
                            'stats': stats,
                            'status': 'success'
                        })
                    else:
                        results.append({
                            'username': username,
                            'status': 'failed',
                            'error': 'Could not fetch stats'
                        })
                except Exception as e:
                    results.append({
                        'username': username,
                        'status': 'error',
                        'error': str(e)
                    })
            
            # Calculate summary stats
            successful = len([r for r in results if r['status'] == 'success'])
            failed = len(results) - successful
            
            return Response({
                'results': results,
                'total_urls': len(usernames),
                'successful': successful,
                'failed': failed
            })
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}", exc_info=True)
            return Response(
                {"detail": f"An error occurred during analysis: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CompanyLeetCodeExportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Export LeetCode analysis history to CSV.
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="leetcode_analysis_{datetime.now().strftime("%Y%m%d")}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Employee', 'LeetCode Username', 'Total Solved', 'Easy', 'Medium', 'Hard', 'Score', 'Analyzed At'])

        history = LeetCodeAnalysisHistory.objects.filter(company=request.user).order_by('-analyzed_at')
        
        for record in history:
            writer.writerow([
                record.employee_identifier,
                record.leetcode_username,
                record.total_solved,
                record.easy_solved,
                record.medium_solved,
                record.hard_solved,
                record.problem_solving_score,
                record.analyzed_at.strftime("%Y-%m-%d %H:%M:%S")
            ])

        return response
