export interface ProxyLog {
  id: number;
  timestamp: string;
  client_ip: string;
  target_host: string;
  target_ip: string;
  status: string;
  request_data: string;
}