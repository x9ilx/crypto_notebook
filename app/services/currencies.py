from models.currency import Currency
from services.files import delete_file

async def delete_image_file_if_exist(currency: Currency) -> str:
    if currency.image_path is not None:
        await delete_file(currency.image_path)
