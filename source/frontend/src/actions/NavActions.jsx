export function toggleRedirect(redirect_id) {
    return {
        type: redirect_id,
        payload: true
    }
}

export function resetRedirect() {
    return {
        type: 'RESET_REDIRECT_STATE'
    }
}