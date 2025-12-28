from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.coding_platform_models import CodingProfile
from api.coding_profile_serializers import CodingProfileSerializer
from api.services.leetcode_service import LeetCodeService
import logging

logger = logging.getLogger(__name__)

class CodingProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CodingProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CodingProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def sync(self, request, pk=None):
        profile = self.get_object()
        if profile.platform != 'leetcode':
            return Response({'error': 'Only LeetCode syncing is supported currently'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            stats = LeetCodeService.get_user_stats(profile.username)
            if stats:
                profile.stats = stats
                profile.last_synced = timezone.now()
                profile.save()
                return Response(CodingProfileSerializer(profile).data)
            return Response({'error': 'Failed to fetch stats from LeetCode'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error syncing profile: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
