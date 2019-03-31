export function toggleRedirect(toAdminPanel) {
    return {
        type: toAdminPanel
    }
}

export function resetRedirect() {
    return {
        type: 'RESET_REDIRECT'
    }
}