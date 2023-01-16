from .wellness import Posture


async def setup(bot):
    await bot.add_cog(Posture(bot))