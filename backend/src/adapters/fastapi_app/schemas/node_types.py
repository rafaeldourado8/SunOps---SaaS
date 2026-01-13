from enum import Enum

class NodeType(str, Enum):
    AGENT_VENDAS = "agent_vendas"
    AGENT_SUPORTE = "agent_suporte"
    WHATSAPP = "whatsapp"
    INVERSOR = "inversor"
    PDF_GENERATOR = "pdf_generator"
    
    @classmethod
    def get_display_name(cls, node_type: str) -> str:
        names = {
            cls.AGENT_VENDAS: "Bot de Vendas",
            cls.AGENT_SUPORTE: "Bot de Suporte",
            cls.WHATSAPP: "WhatsApp",
            cls.INVERSOR: "Monitor Inversor",
            cls.PDF_GENERATOR: "Gerador PDF"
        }
        return names.get(node_type, node_type)
    
    @classmethod
    def get_icon(cls, node_type: str) -> str:
        icons = {
            cls.AGENT_VENDAS: "🏷️",
            cls.AGENT_SUPORTE: "💬",
            cls.WHATSAPP: "📱",
            cls.INVERSOR: "⚡",
            cls.PDF_GENERATOR: "📄"
        }
        return icons.get(node_type, "📦")
