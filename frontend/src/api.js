const BASE_URL = "http://127.0.0.1:9000/api";

export const apiClient = {
  // Save JWT inside client configuration
  setToken(token) {
    localStorage.setItem("token", token);
  },

  getToken() {
    return localStorage.getItem("token");
  },

  logout() {
    localStorage.removeItem("token");
  },

  // Structural header configurations
  getHeaders(isMultipart = false) {
    const headers = {};
    if (!isMultipart) {
      headers["Content-Type"] = "application/json";
    }
    const token = this.getToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
    return headers;
  },

  // Auth Operations
  async register(name, email, password) {
    const res = await fetch(`${BASE_URL}/auth/register`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ name, email, password }),
    });
    if (!res.ok) throw new Error((await res.json()).detail || "Registration failed");
    return res.json();
  },

  async login(email, password) {
    const res = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) throw new Error((await res.json()).detail || "Login failed");
    const data = await res.json();
    this.setToken(data.access_token);
    return data;
  },

  async getMe() {
    const res = await fetch(`${BASE_URL}/auth/me`, {
      method: "GET",
      headers: this.getHeaders(),
    });
    if (!res.ok) throw new Error("Session expired");
    return res.json();
  },

  // Core Processing Pipelines
  async uploadFile(fileFile, language = "en") {
    const formData = new FormData();
    formData.append("file", fileFile);
    formData.append("language", language);

    const res = await fetch(`${BASE_URL}/upload-file`, {
      method: "POST",
      headers: this.getHeaders(true), // true drops Content-Type to allow boundary configurations
      body: formData,
    });
    if (!res.ok) throw new Error((await res.json()).detail || "File processing failed");
    return res.json();
  },

  async processUrl(url, language = "en") {
    const res = await fetch(`${BASE_URL}/process-url`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ source: url, language }),
    });
    if (!res.ok) throw new Error((await res.json()).detail || "URL processing failed");
    return res.json();
  },

  // Chat Execution 
  async askQuestion(meetingId, question) {
    const res = await fetch(`${BASE_URL}/chat/${meetingId}`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ question }),
    });
    if (!res.ok) throw new Error("RAG query failed");
    return res.json();
  }
};