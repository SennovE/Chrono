// import axios from 'axios';

export function getToken(router) {
    const token = localStorage.getItem('chronoJWTToken')
    if (token) {
        router.push({
            name: 'Login Page',
            query: {
              showMessage: 'Войдите в аккаунт'
            }
        })
    }
    return token
}

