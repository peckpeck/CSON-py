#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import json
from pprint import pprint

#if (typeof CSON !== 'object')
#    var CSON = {};
#if (typeof module !== 'undefined')
#    module.exports = CSON;


#(function () {
#    CSON.toJSON = toJSON;
#    CSON.parse = parse;

def charAt(string, index):
  if index >= len(string) or index < 0:
    return None
  return string[index]

#    function isName(char) {
#        return !/\s|,|:|=|"|'|\[|\{|\]|\}|#/.test(char);
#    }
def isName(char):
  return not re.match(r"""\s|,|:|=|"|'|\[|\{|\]|\}|#""", char)

#    function isWS(char) {
#        return /\s/.test(char);
#    }
def isWS(char):
  return re.match(r'\s', char)

#    function isCRLF(char, nextChar) {
#        return char === '\r' && nextChar === '\n';
#    }
def isCRLF(char, nextChar):
  return char == '\r' and nextChar == '\n'

#    function isNameSeparator(char) {
#        return char === ':' || char === '=';
#    }
def isNameSeparator(char):
  return char ==':' or char =='='

#    function isEndOfDQuote(prevChar, char) {
#        return prevChar !== '\\' && char === '\"';
#    }
def isEndOfDQuote(prevChar, char):
  return prevChar != '\\' and char == '\"'

#    function isEndOfSQuote(prevChar, char) {
#        return prevChar !== '\\' && char === '\'';
#    }
def isEndOfSQuote(prevChar, char):
  return prevChar != '\\' and char =='\''

#    function isBeginOfBracket(char) {
#        return char === '[' || char === '{';
#    }
def isBeginOfBracket(char):
  return char == '[' or char == '{'

#    function isEndOfBracket(char) {
#        return char === ']' || char === '}';
#    }
def isEndOfBracket(char):
  return char == ']' or  char == '}'

#    function isBracket(char) {
#        return isBeginOfBracket(char) || isEndOfBracket(char);
#    }
def isBracket(char):
  return isBeginOfBracket(char) or isEndOfBracket(char)

#    function stringToLiteral(string) {
#        string = string.replace('\\', '\\\\');
#        string = string.replace('\b', '\\b');
#        string = string.replace('\f', '\\f');
#        string = string.replace('\n', '\\n');
#        string = string.replace('\r', '\\r');
#        string = string.replace('\t', '\\t');
#        string = string.replace('\"', '\\\"');
#        return string;
#    }
def stringToLiteral(string):
  string = string.replace('\\', '\\\\')
  string = string.replace('\b', '\\b')
  string = string.replace('\f', '\\f')
  string = string.replace('\n', '\\n')
  string = string.replace('\r', '\\r')
  string = string.replace('\t', '\\t')
  string = string.replace('\"', '\\\"')
  return string

#    function tokenize(text) {
def tokenize(text):
#        var tokens = [];
#        var prevChar, currentChar, nextChar;
#        var buffer;
#        var isSQuote;
#        var escapeCount;
#        var verbatimBuffer;
#        var verbatimExit;
  tokens = []
#        for (var i = 0; i < text.length; ++i) {
  i=-1
  while i+1 < len(text):
    i+=1
#            currentChar = text.charAt(i);
#            prevChar = text.charAt(i - 1);
#            nextChar = text.charAt(i + 1);
    currentChar = charAt(text, i)
    prevChar = charAt(text, i-1)
    nextChar = charAt(text, i+1)
#            if (isBracket(currentChar)) tokens.push(currentChar);
    if isBracket(currentChar):
      tokens.append(currentChar)
#            else if (currentChar === ',' || currentChar === '\n') continue;
    elif currentChar == ',' or currentChar == '\n':
      continue
#            else if (isCRLF(currentChar, nextChar)) ++i;
    elif isCRLF(currentChar, nextChar):
      i += 1
#            else if (isNameSeparator(currentChar)) tokens.push(':');
    elif isNameSeparator(currentChar):
      tokens.append(':')
#            else if (currentChar === '\"' || currentChar === '\'') {
    elif currentChar == '\"' or currentChar == '\'':
#                buffer = '';
#                isSQuote = currentChar === '\'';
#                escapeCount = 0;
#                currentChar = text.charAt(++i);
#                prevChar = text.charAt(i - 1);
      buffer = ''
      isSQuote = currentChar == '\''
      escapeCount = 0
      i+=1
      currentChar = charAt(text, i)
      prevChar = charAt(text, i-1)
#                while (!(isSQuote?
#                         isEndOfSQuote(prevChar, currentChar) :
#                         isEndOfDQuote(prevChar, currentChar)) &&
#                       i < text.length) {
      while not (isEndOfSQuote(prevChar, currentChar) if isSQuote else isEndOfDQuote(prevChar, currentChar)):
#                    if (isSQuote &&
#                        currentChar === '\"' &&
#                        (escapeCount % 2) === 0)
#                        buffer += '\\';
        if isSQuote and currentChar == '\"' and (escapeCount % 2) == 0:
          buffer += '\\'
#                    buffer += currentChar;
        if currentChar is not None:
          buffer += currentChar
#                    escapeCount = (currentChar === '\\')? escapeCount + 1 : 0;
        escapeCount = escapeCount + 1 if currentChar == '\\' else 0
#                    currentChar = text.charAt(++i);
        i += 1
        currentChar = charAt(text ,i)
#                    prevChar = text.charAt(i - 1);
        prevChar = charAt(text, i-1)
#                }
#                tokens.push('\"' + buffer + '\"');
      tokens.append('\"' + buffer + '\"')
#            }
#            else if (currentChar === '|') {
    elif currentChar == '|':
#                buffer = '';
#                verbatimBuffer = [];
#                verbatimExit = false;
      buffer = ''
      verbatimBuffer = []
      verbatimExit = False
#                while(i < text.length) {
      while i < len(text):
#                    currentChar = text.charAt(++i);
#                    nextChar = text.charAt(i + 1);
        i += 1
        currentChar = charAt(text, i)
        nextChar = charAt(text, i+1)
#                    if (verbatimExit) {
        if verbatimExit:
#                        if (currentChar === '|') {
          if currentChar == '|':
#                            verbatimExit = false;
#                            continue;
            verbatimExit = False
            continue
#                        }
#                        else if (isCRLF(currentChar, nextChar)) {
          elif isCRLF(currentChar, nextChar):
#                            ++i;
#                            break;
            i += 1
            break
#                        }
#                        else if (currentChar === '\n') break;
          elif currentChar == '\n':
            break
#                        else if (!isWS(currentChar)) {
          elif not isWS(currentChar):
#                            --i;
            i -= 1
#                            break;
            break
#                        }
#                    }
#                    else if (isCRLF(currentChar, nextChar)) {
        elif isCRLF(currentChar, nextChar):
#                        ++i;
          i += 1
#                        verbatimBuffer.push(stringToLiteral(buffer));
#                        buffer = '';
#                        verbatimExit = true;
          verbatimBuffer.append(stringToLiteral(buffer))
          buffer = ''
          verbatimExit = True
#                    }
#                    else if (currentChar === '\n') {
        elif currentChar == '\n':
#                        verbatimBuffer.push(stringToLiteral(buffer));
#                        buffer = '';
#                        verbatimExit = true;
          verbatimBuffer.append(stringToLiteral(buffer))
          buffer = ''
          verbatimExit = True
#                    }
#                    else buffer += currentChar;
        else:
          buffer += currentChar
#                }
#                if (!verbatimExit)
      if not verbatimExit:
#                    verbatimBuffer.push(stringToLiteral(buffer));
        verbatimBuffer.append(stringToLiteral(buffer))
#                buffer = '';
#                tokens.push('\"' + verbatimBuffer.join('\\n') + '\"');
      buffer = ''
      tokens.append('\"' + '\\n'.join(verbatimBuffer) + '\"')
#            }
#            else if (currentChar === '#') {
    elif currentChar == '#':
#                while (i < text.length) {
      while i < len(text):
#                    currentChar = text.charAt(++i);
#                    nextChar = text.charAt(i + 1);
        i+=1
        currentChar = charAt(text, i)
        nextChar = charAt(text, i+1)
#                    if (currentChar === '\n') break;
        if currentChar == '\n':
          break
#                    else if (isCRLF(currentChar, nextChar)) {
        elif isCRLF(currentChar, nextChar):
#                        ++i;
#                        break;
          i+=1
          break
#                    }
#                }
#            }
#            else if (isWS(currentChar)) {
    elif isWS(currentChar):
#                while (isWS(currentChar) && i < text.length)
      while isWS(currentChar) and i < len(text):
#                    currentChar = text.charAt(++i);
        i+=1
        currentChar = charAt(text, i)
#                --i;
      i-=1
#            }
#            else {
    else:
#                if (!isName(nextChar)) {
      if not isName(nextChar):
#                    tokens.push(currentChar);
        tokens.append(currentChar)
#                    continue;
        continue
#                }
#                buffer = currentChar;
      buffer = currentChar
#                while (i < text.length) {
      while i < len(text):
#                    currentChar = text.charAt(++i);
#                    nextChar = text.charAt(i + 1);
#                    buffer += currentChar;
        i+=1
        currentChar = charAt(text, i)
        nextChar = charAt(text, i+1)
        buffer += currentChar
#                    if (!isName(nextChar)) break;
        if not isName(nextChar):
          break
#                }
#                tokens.push(buffer);
      tokens.append(buffer)
#            }
#        }
#        return tokens;
  return tokens
#    }

#        function newline() {
def newline(indent, indentLevel):
#            var result = '\n';
  result = '\n'
#            if (indent === '0') return result;
#            for (var i = 0; i < indentLevel; ++i)
  for i in range(0, indentLevel):
#                result += indent;
    result += indent
#            return result;
  return result
#        }


#    function toJSON(text, indent) {
def toJSON(text, indent):
#        var tokens = tokenize(String(text));
  tokens = tokenize(text)
#        var indentLevel = 0;
  indentLevel = 0
#        if (indent !== '0') {
#            if (!isNaN(parseInt(indent)))
#                indent = Array(parseInt(indent) + 1).join(' ');
#            else if (typeof indent != 'string')
#                indent = indent ? '    ' : false;
#        }

#        function newline() {
#            var result = '\n';
#            if (indent === '0') return result;
#            for (var i = 0; i < indentLevel; ++i)
#                result += indent;
#            return result;
#        }

#        if (!isBeginOfBracket(tokens[0])) {
  if not isBeginOfBracket(charAt(tokens,0)):
#            if (tokens[1] !== undefined) {
    if charAt(tokens,1) is not None:
#                if (tokens[1] === ':') {
      if charAt(tokens,1) == ':':
#                    tokens.unshift('{');
#                    tokens.push('}');
        tokens.insert(0, '{')
        tokens.append('}')
#                }
#                else {
      else:
#                    tokens.unshift('[');
#                    tokens.push(']');
        tokens.insert('[')
        tokens.append(']')
#                }
#            }
#        }
#        for (var i = 0; i < tokens.length; ++i) {
  for i in range(0, len(tokens)):
#            var token = tokens[i];
    token = charAt(tokens,i)
#            var nextToken = tokens[i + 1];
    nextToken = charAt(tokens,i+1)
#            if (indent) {
    if len(indent) != 0:
#                if (token === ':') tokens[i] += ' ';
      if token == ':':
        tokens[i] += ' '
#                if (isBeginOfBracket(token.charAt())) ++indentLevel;
      if isBeginOfBracket(charAt(token, 0)):
        indentLevel += 1
#                if (isEndOfBracket(token.charAt())) --indentLevel;
      if isEndOfBracket(charAt(token, 0)):
        indentLevel -= 1
#            }
#            if (isName(token.charAt()) && tokens[i + 1] === ':')
    if isName(charAt(token, 0)) and charAt(tokens, i + 1) == ':':
#                tokens[i] = '\"' + tokens[i] + '\"';
      tokens[i] = '\"' + tokens[i] + '\"'
#            if (!/\[|\{|:/.test(tokens[i].charAt()) &&
#                typeof nextToken !== 'undefined' &&
#                !/\]|\}|:/.test(nextToken.charAt())) {
    if not re.search(r'\[|\{|:', charAt(tokens[i], 0)) and nextToken is not None and not re.search(r'\]|\}|:', charAt(nextToken, 0)):
#                tokens[i] += ',';
      tokens[i] += ','
#                if (indent) tokens[i] += newline();
      if len(indent) != 0:
        tokens[i] += newline(indent, indentLevel)
#            }
#        }
#        if (indent) {
  if len(indent) != 0:
#            for (i = 0; i < tokens.length; ++i) {
    for i in range(0, len(tokens)):
#                var token = tokens[i];
      token = charAt(tokens, i)
#                var prevToken = tokens[i - 1];
      prevToken = charAt(tokens, i - 1)
#                var nextToken = tokens[i + 1];
      nextToken = charAt(tokens, i + 1)
#                if (isBeginOfBracket(token.charAt())) {
      if isBeginOfBracket(charAt(token, 0)):
#                    ++indentLevel;
        indentLevel+=1
#                    if (nextToken && !isEndOfBracket(nextToken.charAt()))
        if nextToken is not None and not isEndOfBracket(charAt(nextToken, 0)):
#                        tokens[i] += newline();
          tokens[i] += newline(indent, indentLevel)
#                }
#                if (isEndOfBracket(token.charAt())) {
      if isEndOfBracket(charAt(token, 0)):
#                    --indentLevel;
        indentLevel-=1
#                    if (prevToken && !isBeginOfBracket(prevToken.charAt()))
        if prevToken is not None and not isBeginOfBracket(charAt(prevToken, 0)):
#                        tokens[i] = newline() + token;
          tokens[i] = newline(indent, indentLevel) + token
#                }
#            }
#        }
#        return tokens.join('');
  return ''.join(tokens)
#    }

#    function parse(csonString) {
def parse(csonString):
  return json.loads(toJSON(csonString, '  '))
#        return JSON.parse(toJSON(csonString));
#    }
#})();


string=u"""
# CSON example
pi: 3.141592
e = 2.718281828, 'foo': 'bar'
"nested" = ["JSON array",
            {and = "JSON object"},
            "with a trailing comma", # yes!
            # yes, the comment can be inside JSON arrays/objects as well
           ]
"verbatim": |a verbatim string
            |  keeps the preceding whitespace
            |    and joins all lines with `\\n`
            |      as you see, no escape sequence is processed
            |        and this string does not have a trailing \\n -->
i18n: {
  한국어: "Korean"
  日本語: "Japanese"
  汉语-or-漢語: "Chinese"
  ᏣᎳᎩ: "Cherokee"
}"""

print(string)
print("-----------------------")
print(toJSON(string, '  '))
print("-----------------------")
#pprint(parse(string))
