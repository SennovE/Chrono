import axios from 'axios';

function redirectToLogin(router) {
    router.push({
        name: 'Login Page',
    })
}

function getToken(router) {
    const token = localStorage.getItem('chronoJWTToken')
    if (!token) {
        redirectToLogin(router)
    }
    return token
}

export async function authUser(router) {
    try {
        const token = getToken(router);
        const response = await axios.get('http://localhost:8080/api/v1/user/me', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })
        return response.data
    } catch (error) {
        redirectToLogin(router)
    }
}