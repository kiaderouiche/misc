(require-package 'go-mode)

(defun my-go-mode-hook ()
  ; Use goimports instead of go-fmt
  (let ((goimports (executable-find "goimports")))
    (when goimports
      (setq gofmt-command goimports)))
  ; Call Gofmt before saving
  (add-hook 'before-save-hook 'gofmt-before-save)
  ; Customize compile command to run go build
  (if (not (string-match "go" compile-command))
      (set (make-local-variable 'compile-command)
           "go generate && go build -v && go test -v && go tool vet"))
  ; Go oracle
  ;;(load-file "$GOPATH/src/golang.org/x/tools/cmd/oracle/oracle.el")
  ; Godef jump key binding
  (local-set-key (kbd "M-.") 'godef-jump)
  (local-set-key (kbd "M-*") 'pop-tag-mark)
)
(add-hook 'go-mode-hook 'my-go-mode-hook)

(require-package 'go-projectile)
(require-package 'golint)
(require-package 'go-gopath)
(require-package 'gotest)

(provide 'init-go)


