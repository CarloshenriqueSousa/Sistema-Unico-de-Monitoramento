from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from .models import Estudante


def _profile_from_estudante(estudante: Estudante):
    # Build a minimal DotsProfile-like structure expected by frontend
    skills = [
        {"name": "humanas", "level": round(estudante.media_humanas / 10), "verified": True, "category": "academico"},
        {"name": "linguagens", "level": round(estudante.media_linguagens / 10), "verified": True, "category": "academico"},
        {"name": "exatas", "level": round(estudante.media_exatas / 10), "verified": True, "category": "academico"},
    ]
    return {
        "id": estudante.id,
        "studentId": estudante.id,
        "achievements": {
            "academic": [],
            "sports": [],
            "arts": [],
            "community": [],
            "social": [],
            "technical": [],
        },
        "skills": skills,
        "badges": [],
        "portfolio": [],
        "visibilitySettings": {
            "public": False,
            "allowedViewers": []
        }
    }


class DotsProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id: int):
        try:
            estudante = Estudante.objects.get(pk=user_id)
        except Estudante.DoesNotExist:
            return Response({"message": "Estudante não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(_profile_from_estudante(estudante))


class DotsLeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        top = Estudante.objects.order_by('-dots_pontos')[:20]
        data = [
            {
                "studentId": e.id,
                "studentName": e.usuario.nome,
                "overallScore": e.dots_pontos,
                "topSkills": [
                    {"name": "humanas", "level": round(e.media_humanas / 10), "verified": True},
                    {"name": "linguagens", "level": round(e.media_linguagens / 10), "verified": True},
                    {"name": "exatas", "level": round(e.media_exatas / 10), "verified": True},
                ],
                "totalAchievements": 0,
                "rank": idx + 1,
            }
            for idx, e in enumerate(top)
        ]
        return Response(data)


class DotsAchievementsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Accept any payload and return it with an id and awardedAt to unblock UI
        payload = dict(request.data or {})
        payload.update({
            "id": int(timezone.now().timestamp()),
            "awardedAt": timezone.now().isoformat(),
        })
        return Response(payload, status=status.HTTP_201_CREATED)


class DotsSkillView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, student_id: int):
        skill = request.data.get('skill')
        value = request.data.get('value')
        if not isinstance(skill, str) or not isinstance(value, (int, float)):
            return Response({"message": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            estudante = Estudante.objects.get(pk=student_id)
        except Estudante.DoesNotExist:
            return Response({"message": "Estudante não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        # Map to medias roughly for demo purposes
        if skill.lower() == 'humanas':
            estudante.media_humanas = max(0, min(100, value * 10))
        elif skill.lower() == 'linguagens':
            estudante.media_linguagens = max(0, min(100, value * 10))
        elif skill.lower() == 'exatas':
            estudante.media_exatas = max(0, min(100, value * 10))
        estudante.save()
        return Response(_profile_from_estudante(estudante))


class DotsSkillBulkView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, student_id: int):
        skills = request.data.get('skills') or []
        try:
            estudante = Estudante.objects.get(pk=student_id)
        except Estudante.DoesNotExist:
            return Response({"message": "Estudante não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        for item in skills:
            name = (item or {}).get('name', '').lower()
            value = (item or {}).get('value', 0)
            if name == 'humanas':
                estudante.media_humanas = max(0, min(100, int(value) * 10))
            elif name == 'linguagens':
                estudante.media_linguagens = max(0, min(100, int(value) * 10))
            elif name == 'exatas':
                estudante.media_exatas = max(0, min(100, int(value) * 10))
        estudante.save()
        return Response(_profile_from_estudante(estudante))


class DotsSyncView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, service: str):
        student_id = request.data.get('studentId')
        try:
            estudante = Estudante.objects.get(pk=student_id)
        except Estudante.DoesNotExist:
            return Response({"message": "Estudante não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        # Simulate sync: just bump points
        estudante.dots_pontos += 5
        estudante.save()
        return Response(_profile_from_estudante(estudante))


