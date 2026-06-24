# Fluxos de Sistema

## Fluxo de Autenticação

```{mermaid}
sequenceDiagram
    participant U as Usuário
    participant S as Sistema
    participant L as Syslog

    U->>S: Informa credenciais (usuário/senha)
    S->>S: Valida credenciais
    alt Credenciais válidas
        S->>U: Concede acesso
        S->>L: Log: "LOGIN_SUCCESS - usuário autenticado"
    else Credenciais inválidas
        S->>U: Nega acesso
        S->>L: Log: "LOGIN_FAILURE - tentativa inválida"
        Note over S: Se ≥ 5 falhas em 1 minuto<br/>bloquear temporariamente
    end
```

## Fluxo de Operações em Tarefas (CRUD)

```{mermaid}
sequenceDiagram
    participant U as Usuário
    participant S as Sistema
    participant D as Banco de Dados
    participant L as Syslog

    U->>S: Requisição (criar/editar/excluir/visualizar)
    S->>S: Verifica autenticação
    alt Não autenticado
        S->>U: Redireciona para login
        S->>L: Log: "UNAUTHORIZED_ACCESS - requisição bloqueada"
    else Autenticado
        alt Ação válida
            S->>D: Executa operação
            D-->>S: Resultado
            S-->>U: Resposta
            S->>L: Log: "OPERATION_SUCCESS - {ação} - {id_tarefa}"
        else Violação (ex: editar tarefa de outro usuário)
            S->>U: Erro de permissão
            S->>L: Log: "SECURITY_VIOLATION - tentativa de acesso não autorizado a recurso"
        end
    end
```

## Fluxo de Logging de Violação de Segurança

```{mermaid}
flowchart TD
    A[Requisição recebida] --> B{Autenticado?}
    B -->|Não| C[Bloquear requisição]
    C --> D[Log: UNAUTHORIZED_ACCESS]
    B -->|Sim| E{Autorizado?}
    E -->|Não| F[Negar operação]
    F --> G[Log: SECURITY_VIOLATION]
    E -->|Sim| H{Entrada válida?}
    H -->|Não| I[Rejeitar requisição]
    I --> J[Log: INVALID_INPUT]
    H -->|Sim| K[Executar operação]
    K --> L[Log: OPERATION_SUCCESS]
```

## Eventos de Log (Syslog)

| Evento | Severidade | Mensagem |
| --- | --- | --- |
| Login bem-sucedido | INFO | `LOGIN_SUCCESS user=<username> ip=<remote_addr>` |
| Falha de login | WARNING | `LOGIN_FAILURE user=<username> ip=<remote_addr> attempts=<count>` |
| Acesso sem autenticação | WARNING | `UNAUTHORIZED_ACCESS endpoint=<path> ip=<remote_addr>` |
| Violação de permissão | WARNING | `SECURITY_VIOLATION user=<username> action=<operation> resource=<id>` |
| Entrada maliciosa detectada | WARNING | `INVALID_INPUT user=<username> field=<field> value=<sanitized_input>` |
| CRUD realizado | INFO | `OPERATION_SUCCESS user=<username> action=<operation> task_id=<id>` |
| Rate limit excedido | WARNING | `RATE_LIMIT_EXCEEDED ip=<remote_addr> endpoint=<path>` |
