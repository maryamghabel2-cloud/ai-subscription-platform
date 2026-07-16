// Next.js API route for health check
import { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({
    status: 'ok',
    message: 'AI Subscription Platform API',
    timestamp: new Date().toISOString()
  });
}
