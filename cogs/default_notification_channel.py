import discord
from discord.ext import commands
import sqlite3


class DefaultNotificationChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def show_default_notification_channel_menu(self, interaction: discord.Interaction):
        """
        Display the menu for managing the Default Notification Channel.
        """
        try:
            alliance_id = 1  # Example alliance_id; replace this dynamically if needed
            current_channel = await self.get_default_notification_channel(interaction.guild.id, alliance_id)

            embed = discord.Embed(
                title="📢 Default Notification Channel Setup",
                description=(
                    "Use this menu to select or manage the default notification channel for alliance events."
                    " The selected channel will be used by features like notifications.\n\n"
                    f"**Current Channel:** {current_channel.mention if current_channel else 'Not Set'}"
                ),
                color=discord.Color.blue()
            )

            view = DefaultNotificationChannelView(self, alliance_id)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

        except Exception as e:
            print(f"Error in show_default_notification_channel_menu: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while opening the Default Notification Channel menu.",
                ephemeral=True
            )

    async def get_default_notification_channel(self, guild_id, alliance_id):
        """
        Fetch the currently configured Default Notification Channel from the database.
        """
        try:
            with sqlite3.connect('db/alliance.sqlite') as db:
                cursor = db.cursor()
                cursor.execute(
                    "SELECT default_notification_channel FROM alliancesettings WHERE alliance_id = ?",
                    (alliance_id,)
                )
                result = cursor.fetchone()

            if result and result[0]:
                return discord.utils.get(await self.bot.fetch_guild(guild_id).fetch_channels(), id=result[0])
            return None
        except Exception as e:
            print(f"Error fetching default notification channel: {e}")
            return None

    async def set_default_notification_channel(self, alliance_id, channel_id):
        """
        Save the Default Notification Channel to the database.
        """
        try:
            with sqlite3.connect('db/alliance.sqlite') as db:
                cursor = db.cursor()
                cursor.execute('''
                    INSERT INTO alliancesettings (alliance_id, default_notification_channel)
                    VALUES (?, ?)
                    ON CONFLICT(alliance_id) DO UPDATE SET
                    default_notification_channel = excluded.default_notification_channel
                ''', (alliance_id, channel_id))
                db.commit()
        except Exception as e:
            print(f"Error saving default notification channel to the database: {e}")


class DefaultNotificationChannelView(discord.ui.View):
    """
    View for selecting the Default Notification Channel.
    """

    def __init__(self, cog, alliance_id):
        super().__init__(timeout=None)
        self.cog = cog
        self.alliance_id = alliance_id

    @discord.ui.select(
        placeholder="Select a default channel",
        options=[],
        custom_id="default_notification_channel_select"
    )
    async def select_channel(self, interaction: discord.Interaction, select):
        """
        Handle selecting a new Default Notification Channel.
        """
        try:
            selected_channel_id = int(select.values[0])
            await self.cog.set_default_notification_channel(self.alliance_id, selected_channel_id)

            success_embed = discord.Embed(
                title="✅ Channel Updated!",
                description=f"The **Default Notification Channel** has been updated to {interaction.guild.get_channel(selected_channel_id).mention}.",
                color=discord.Color.green()
            )
            await interaction.response.edit_message(embed=success_embed, view=None)

        except Exception as e:
            print(f"Error processing channel selection: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while setting the Default Notification Channel.",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(DefaultNotificationChannel(bot))