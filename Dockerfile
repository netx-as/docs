FROM mcr.microsoft.com/dotnet/sdk:8.0 AS docfx-build
WORKDIR /docfx

# Install DocFX
RUN dotnet tool install -g docfx
ENV PATH="$PATH:/root/.dotnet/tools"

COPY . .
RUN docfx build

FROM nginx:alpine
COPY --from=docfx-build /docfx/_site /usr/share/nginx/html
