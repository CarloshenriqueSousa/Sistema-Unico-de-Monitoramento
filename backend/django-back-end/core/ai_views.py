from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from estudantes.models import Estudante


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat(request):
    """
    Minimal chat endpoint to unblock frontend. Echoes message and returns a canned reply.
    Expected payload: { "role": "user|system", "message": str, "context": str }
    """
    message = request.data.get('message') or ''
    if not isinstance(message, str) or not message.strip():
        return Response({"message": "Mensagem inválida"}, status=status.HTTP_400_BAD_REQUEST)

    reply = {
        "id": int(timezone.now().timestamp()),
        "role": "assistant",
        "message": f"Recebi sua mensagem: {message.strip()}",
        "context": request.data.get('context') or '',
        "timestamp": timezone.now().isoformat()
    }
    return Response(reply, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_notes(request):
    """Generate study notes placeholder."""
    subject = request.data.get('subject') or 'Assunto'
    topics = request.data.get('topics') or []
    notes = (
        f"Resumo de {subject}.\n\n" +
        ("Tópicos: " + ", ".join(topics) + "\n\n" if isinstance(topics, list) and topics else '') +
        "1) Conceitos principais...\n2) Exemplos...\n3) Dicas de estudo...\n"
    )
    return Response({"notes": notes}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analyze_dots(request, user_id: int):
    """Return a simple analysis for the given student id."""
    try:
        estudante = Estudante.objects.get(pk=user_id)
    except Estudante.DoesNotExist:
        return Response({"message": "Estudante não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    analysis = {
        "studentId": estudante.id,
        "overallScore": estudante.dots_pontos,
        "summary": f"Análise inicial para {estudante.usuario.nome} com {estudante.dots_pontos} pontos.",
        "strengths": ["organização", "participação"],
        "weaknesses": ["revisão"],
        "recommendations": [
            "Criar rotina de revisão semanal",
            "Praticar exercícios focados nas áreas com menor média"
        ],
        "generatedAt": timezone.now().isoformat(),
    }
    return Response(analysis, status=status.HTTP_200_OK)


