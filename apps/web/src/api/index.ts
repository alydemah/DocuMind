import { DocuMindClient } from "@documind/api-client";

const baseURL = import.meta.env.VITE_API_URL || "";

export const api = new DocuMindClient({ baseURL });
export default api;
