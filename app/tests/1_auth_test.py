REGISTER_URL = '/auth/register'


class TestAuth:
    async def test_register(self, noauth_client):
        user_data = {
            'email': 'test@test.com',
            'password': 'test',
        }
        response = await noauth_client.post(REGISTER_URL, json=user_data)
        assert (
            response.status_code == 201,
            'Запрос должен вернуть ответ 201 - CREATED.',
        )

        data = response.json()
        expected_keys = {
            'id',
            'email',
            'is_active',
            'is_superuser',
            'is_verified',
        }
        missing_keys = expected_keys - data.keys()
        assert not missing_keys, (
            f'В ответе на корректный запрос не хватает следующих ключей: '
            f'`{"`, `".join(missing_keys)}`'
        )
        data.pop('id')
        assert data == {
            'email': user_data['email'],
            'is_active': True,
            'is_superuser': False,
            'is_verified': False,
        }, 'При регистрации пользователя тело ответа отличается от ожидаемого.'
