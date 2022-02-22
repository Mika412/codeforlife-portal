import React from 'react'
import LogInButton from './LogInButton'
import RegisterButton from './RegisterButton'
import { NotLoggedInStyled } from './LogInButtonStyled'

const NotLoggedIn: React.FC = () => {
    return (
        <NotLoggedInStyled>
            <RegisterButton />
            <LogInButton />
        </NotLoggedInStyled>
    )
}

export default NotLoggedIn