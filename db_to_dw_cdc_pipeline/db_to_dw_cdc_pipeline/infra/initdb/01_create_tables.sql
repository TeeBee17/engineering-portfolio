CREATE TABLE IF NOT EXISTS public.customers (
  customer_id VARCHAR(64) PRIMARY KEY,
  email VARCHAR(200) NOT NULL,
  plan VARCHAR(30) NOT NULL DEFAULT 'FREE',
  country VARCHAR(2) NOT NULL DEFAULT 'NG',
  status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO public.customers(customer_id, email, plan, country, status)
VALUES
('c-001', 'a@example.com', 'FREE', 'NG', 'ACTIVE'),
('c-002', 'b@example.com', 'PRO',  'NG', 'ACTIVE')
ON CONFLICT (customer_id) DO NOTHING;
