(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

; Some utility functions that you may find useful to implement.
(define (map proc items)
  (if (null? items)
   '()
   (cons (proc (car items)) (map proc (cdr items))))
  )

(define (cons-all first rests)
  (map (lambda (temp) (cons first temp)) rests))

(define (zip pairs)
  (list (map (lambda (pairs) (car pairs)) pairs) (map (lambda (pairs) (cadr pairs)) pairs))
)
;; Problem 17
;; Returns a list of two-element lists

(define (enumerate s)
	(define (helper_fn index lst)
		(if (null? lst) nil
			(cons (list index (car lst)) (helper_fn (+ index 1) (cdr lst)))))
	(helper_fn 0 s)
)

;; Problem 18
;; List all ways to make change for TOTAL with DENOMS
(define (list-change total denoms)
	(cond ((<= total 0) '())
		((null? denoms) '())
		(else
			(if (= total (car denoms)) (define eq_first (list(list(car denoms)))) (define eq_first '()))
			(define rest (list-change (- total (car denoms)) denoms))
			(if (null? rest) (define used '()) (define used (cons-all (car denoms) rest)))
			(define rest_of_list (list-change total (cdr denoms)))
			(append eq_first used rest_of_list)
		)
	)
)


;; Problem 19
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
        expr
         )
        ((quoted? expr)
         expr
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           (cons form (cons (map let-to-lambda params) (map let-to-lambda body)))
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
         	(define zip_values (zip values))
         	(define params (map let-to-lambda (car zip_values)))
         	(define params_values (map  let-to-lambda (cadr zip_values)))
         	(cons (cons 'lambda (cons params (map let-to-lambda body))) params_values)
           ))
        (else
         (map let-to-lambda expr)
         )))
