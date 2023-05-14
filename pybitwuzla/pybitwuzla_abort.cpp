// Generated from https://github.com/bitwuzla/bitwuzla at 1230d80

/***
 * Bitwuzla: Satisfiability Modulo Theories (SMT) solver.
 *
 * This file is part of Bitwuzla.
 *
 * Copyright (C) 2007-2022 by the authors listed in the AUTHORS file.
 *
 * See COPYING for more information on using this software.
 */

#include "pybitwuzla_abort.h"

#include <stdexcept>

void
pybitwuzla_abort_fun(const char* msg)
{
  throw std::runtime_error(msg);
}

const char*
pybitwuzla_get_err_msg()
{
  try
  {
    throw;
  }
  catch (const std::runtime_error& e)
  {
    return e.what();
  }
}
