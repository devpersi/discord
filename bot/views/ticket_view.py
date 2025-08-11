import logging

import discord
from bot.views.base_view import BaseView
from bot.modals.ticket_modal import TicketModal

logger = logging.getLogger(__name__)

class TicketView(BaseView):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=300) # 5 minutes timeout

    @discord.ui.button(
        label="Επικύρωσε το εισιτήριό σου! | Claim your ticket!", 
        style=discord.ButtonStyle.blurple, 
        custom_id="claim_ticket",
        emoji="🎟️"
    )
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = TicketModal(title="Επικύρωση Εισιτηρίου | Ticket Verification")
        await interaction.response.send_modal(modal)
        await modal.wait()
        if modal.success:
            button.label = "Το εισιτήριο επικυρώθηκε | Ticket Claimed"
            button.style = discord.ButtonStyle.success
            button.emoji = "✅"
            button.disabled = True
        await self._edit(view=self)
        
    async def on_timeout(self) -> None:
        btn = self.children[0]
        if isinstance(btn, discord.ui.Button):
            btn.label = "Η επικύρωση απέτυχε | Claim Failed"
            btn.style = discord.ButtonStyle.danger
            btn.emoji = "❌"
        await super().on_timeout()
