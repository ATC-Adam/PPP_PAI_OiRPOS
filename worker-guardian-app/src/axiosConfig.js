
import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  withCredentials: true, // Dołączaj ciasteczka do każdego żądania
});

export default axiosInstance;