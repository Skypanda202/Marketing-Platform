import api from "./client";

export const authService = {
  login: (payload) => api.post("/auth/", payload),
  register: (payload) => api.post("/auth/register/", payload),
  me: () => api.get("/auth/me/"),
  logout: (refresh) => api.post("/auth/logout/", { refresh }),
  forgotPassword: (email) => api.post("/auth/forgot-password/", { email }),
};

export const campaignService = {
  list: (params) => api.get("/campaigns/", { params }),
  create: (payload) => api.post("/campaigns/", payload),
  update: (id, payload) => api.patch(`/campaigns/${id}/`, payload),
  remove: (id) => api.delete(`/campaigns/${id}/`),
  detail: (id) => api.get(`/campaigns/${id}/`),
};

export const influencerService = {
  list: (params) => api.get("/influencers/", { params }),
  update: (id, payload) => api.patch(`/influencers/${id}/`, payload),
};

export const invitationService = {
  list: (params) => api.get("/invitations/", { params }),
  create: (payload) => api.post("/invitations/", payload),
  accept: (id) => api.post(`/invitations/${id}/accept/`),
  reject: (id) => api.post(`/invitations/${id}/reject/`),
  submitContent: (id, payload) => api.post(`/invitations/${id}/submit_content/`, payload),
};

export const analyticsService = {
  overview: () => api.get("/analytics/overview/"),
  list: (params) => api.get("/analytics/", { params }),
};

export const communicationService = {
  messages: (params) => api.get("/messages/", { params }),
  send: (payload) => api.post("/messages/", payload),
  notifications: () => api.get("/notifications/"),
};

export const aiService = {
  recommendations: () => api.get("/ai/recommendations/"),
  sentiment: (text) => api.post("/ai/sentiment/", { text }),
  fakeEngagement: (payload) => api.post("/ai/fake_engagement/", payload),
};

export const feedService = {
  list: (params) => api.get("/feed/", { params }),
  create: (payload) => api.post("/feed/", payload),
  like: (id) => api.post(`/feed/${id}/like/`),
  unlike: (id) => api.post(`/feed/${id}/unlike/`),
};

export const integrationService = {
  connections: () => api.get("/integrations/connections/"),
  createConnection: (payload) => api.post("/integrations/connections/", payload),
  launches: () => api.get("/integrations/launches/"),
  createLaunch: (payload) => api.post("/integrations/launches/", payload),
  submitLaunch: (id) => api.post(`/integrations/launches/${id}/submit/`),
  metaAuthUrl: () => api.get("/integrations/oauth/meta/start/"),
  googleAuthUrl: () => api.get("/integrations/oauth/google/start/"),
};
