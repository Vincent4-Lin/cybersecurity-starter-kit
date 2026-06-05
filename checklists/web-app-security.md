# Web Application Security Checklist

This checklist is based on common AppSec review areas. It is not a replacement for a full threat model or professional security review.

## Authentication

- [ ] Passwords are hashed with a modern password hashing algorithm.
- [ ] Multi-factor authentication is supported for sensitive accounts.
- [ ] Password reset tokens expire and are single-use.
- [ ] Session cookies use `HttpOnly`, `Secure`, and appropriate `SameSite` settings.

## Authorization

- [ ] Server-side authorization checks protect every sensitive action.
- [ ] Users cannot access another user's records by changing IDs.
- [ ] Admin-only actions are enforced on the server.
- [ ] Object-level permissions are tested.

## Input And Output Handling

- [ ] User input is validated on the server.
- [ ] SQL queries use parameterized statements.
- [ ] HTML output is escaped by default.
- [ ] File uploads validate type, size, and storage location.

## Configuration

- [ ] Debug mode is disabled in production.
- [ ] Error messages do not leak secrets or internals.
- [ ] Security headers are configured.
- [ ] TLS is enforced.

## Dependencies

- [ ] Dependencies are scanned for known vulnerabilities.
- [ ] Lockfiles are kept up to date.
- [ ] Unused packages are removed.

## Logging And Monitoring

- [ ] Authentication failures are logged.
- [ ] Privileged actions are logged.
- [ ] Logs avoid sensitive data.
- [ ] Alerts exist for suspicious behavior.

