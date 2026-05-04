import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  token: localStorage.getItem('clairo_token') || null,
  name: localStorage.getItem('clairo_name') || null,
}

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setCredentials(state, action) {
      state.token = action.payload.token
      state.name = action.payload.name
      localStorage.setItem('clairo_token', action.payload.token)
      localStorage.setItem('clairo_name', action.payload.name)
    },
    logout(state) {
      state.token = null
      state.name = null
      localStorage.removeItem('clairo_token')
      localStorage.removeItem('clairo_name')
    },
  },
})

export const { setCredentials, logout } = authSlice.actions
export default authSlice.reducer