# Stage 1: Build Rust extension and install Python dependencies
FROM python:3.13-slim-bookworm AS builder

# Install Rust toolchain
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
ENV PATH="/root/.cargo/bin:${PATH}"

# Install uv (Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:/root/.local/bin:${PATH}"

WORKDIR /app

# Copy pyproject.toml, README.md and Cargo.toml first to leverage Docker cache
COPY pyproject.toml uv.lock README.md ./
COPY Cargo.toml Cargo.lock ./

# Copy Rust source and Python source
COPY src ./src

# Install maturin and then build the Rust extension and install Python dependencies
RUN pip install maturin
RUN maturin build --release --out target/wheels && \
    uv pip install --system target/wheels/*.whl && \
    uv pip install --system .

# Stage 2: Runtime image
FROM python:3.13-slim-bookworm

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /app/src /app/src
COPY --from=builder /app/pyproject.toml /app/uv.lock /app/Cargo.toml /app/Cargo.lock ./

# Ensure the 'memu' package is discoverable
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Command to run the memu server. This assumes `memu-server` starts a web server.
# The actual port might need adjustment based on memu's configuration.
EXPOSE 8000
CMD ["memu-server"]
