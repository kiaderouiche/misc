package main

//
// find rational approximation to given real number
// Inspired to: http://www.ics.uci.edu/~eppstein/numth/frap.c
//
// K.I.A.Derouiche / NetBSD Project / 18 Sep 2016
//
// usage: a.out r d
//   r is real number to approx
//   d is the maximum denominator allowed
//
// based on the theory of continued fractions
// if x = a1 + 1/(a2 + 1/(a3 + 1/(a4 + ...)))
// then best approximation is found by truncating this series
// (with some adjustments in the last term).
//
// Note the fraction can be recovered as the first column of the matrix
//  ( a1 1 ) ( a2 1 ) ( a3 1 ) ...
//  ( 1  0 ) ( 1  0 ) ( 1  0 )
// Instead of keeping the sequence of continued fraction terms,
// we just keep the last partial product of these matrices.
//

func main(){
  var x, startx float64
  var maxden, ai float64
}
